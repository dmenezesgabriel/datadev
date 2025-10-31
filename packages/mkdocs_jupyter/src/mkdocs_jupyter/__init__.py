"""
https://www.mkdocs.org/dev-guide/plugins/#events
"""

import hashlib
import json
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict

import jupytext  # type: ignore
import nbconvert
import nbformat
from markdownify import markdownify as md  # type: ignore
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger()


class HtmlOutputToMarkdownProcessor(Preprocessor):

    def preprocess_cell(
        self, cell: NotebookNode, resources: Dict[str, Any], index: int
    ) -> tuple[NotebookNode, Dict[str, Any]]:
        if cell.cell_type == "code" and cell.get("outputs"):
            for output in cell.outputs:
                if (
                    "data" in output
                    and "text/html" in output["data"]
                    and "table" in output["data"]["text/html"]
                ):
                    html_content = "".join(output["data"]["text/html"])
                    anchor_tag = "a"
                    markdown_content = md(html_content, strip=[anchor_tag])
                    output["data"]["text/markdown"] = markdown_content
                    del output["data"]["text/html"]
                elif (
                    "data" in output
                    and output.output_type
                    in ("execute_result", "display_data")
                    and "text/plain" in output["data"]
                    and "text/latex" not in output["data"]
                ):
                    plain_text = "".join(output["data"]["text/plain"])
                    fenced_code_block = (
                        "<div class='result' markdown>\n"
                        f"``` linenums='0'\n{plain_text}\n```"
                        "\n</div>"
                    )
                    output["data"]["text/markdown"] = fenced_code_block

                if (
                    "data" in output
                    and "application/vnd.vegalite.v5+json" in output["data"]
                ):
                    json_content = output["data"][
                        "application/vnd.vegalite.v5+json"
                    ]
                    markdown_content = (
                        f"```vegalite \n{json.dumps(json_content)}\n```"
                    )
                    output["data"]["text/markdown"] = markdown_content
                    del output["data"]["application/vnd.vegalite.v5+json"]

        return cell, resources


class MkDocsJupyterPlugin(BasePlugin):
    config_scheme = (
        ("root_dir", config_options.Type(str, default=".")),
        ("template_file", config_options.Type(str, default=None)),
    )

    root_dir: Path
    docs_dir: Path
    exporter: MarkdownExporter
    notebook_mappings: Dict[str, str]
    cache_dir: Path

    def _walk_nav(self, items):
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            for k, v in item.items():
                if isinstance(v, list):
                    self._walk_nav(v)
                if isinstance(v, str) and (
                    v.endswith(".ipynb") or v.endswith(".py")
                ):
                    # The target Markdown file path is always the original path with .md extension
                    md_path = str(Path(v).with_suffix(".md"))
                    # Map the resulting .md path back to the original .ipynb or .py file
                    self.notebook_mappings[md_path] = v
                    # Update the nav item to point to the .md file
                    items[i][k] = md_path

    def _get_source_hash(self, nb_full_path: Path) -> str:
        """Get hash of source notebook file for cache validation"""
        try:
            mtime = nb_full_path.stat().st_mtime
            size = nb_full_path.stat().st_size
            return hashlib.md5(f"{mtime}:{size}".encode()).hexdigest()
        except Exception:
            return ""

    def _read_cache(self, cache_file: Path) -> Dict[str, Any]:
        """Read cache metadata"""
        if not cache_file.exists():
            return {}
        try:
            return json.loads(cache_file.read_text())
        except Exception:
            return {}

    def _write_cache(self, cache_file: Path, data: Dict[str, Any]):
        """Write cache metadata"""
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(data))

    def _register_file(self, files, path, config):
        """Register a file with MkDocs if not already registered"""
        existing_file = files.get_file_from_path(path)
        if existing_file:
            return existing_file

        new_file = File(
            path=path,
            src_dir=str(self.docs_dir),
            dest_dir=config["site_dir"],
            use_directory_urls=config.get("use_directory_urls", True),
        )
        files.append(new_file)
        return new_file

    def on_config(self, config):
        logger.info("on_config triggered")
        self.root_dir = Path(self.config.get("root_dir")).resolve()
        self.docs_dir = Path(config["docs_dir"]).resolve()
        self.cache_dir = self.docs_dir / ".notebook_cache"

        template_file = self.config.get("template_file")

        nbconvert_templates_dir = (
            Path(os.path.dirname(nbconvert.__file__)) / "templates"
        )
        preprocessors_list = [HtmlOutputToMarkdownProcessor]

        if template_file:
            custom_template_path = Path(template_file).resolve()
            extra_template_paths = [
                str(custom_template_path.parent),
                str(nbconvert_templates_dir),
            ]

            self.exporter = MarkdownExporter(
                template_file=str(custom_template_path.name),
                extra_template_paths=extra_template_paths,
                preprocessors=preprocessors_list,
            )
        else:
            self.exporter = MarkdownExporter(preprocessors=preprocessors_list)

        self.notebook_mappings = {}
        self._walk_nav(config["nav"])
        return config

    def on_files(self, files, config):
        logger.info("on_files triggered")
        include_pattern = re.compile(r'--8<--\s*["\']([^"\']+)["\']')

        for md_path, nb_path in self.notebook_mappings.items():
            nb_full_path = (self.root_dir / nb_path).resolve()

            if not nb_full_path.exists():
                logger.warning(
                    f"notebook/jupytext file {nb_path} not found at "
                    f"{nb_full_path}"
                )
                continue

            # Check cache before expensive operations
            source_hash = self._get_source_hash(nb_full_path)
            cache_file = (
                self.cache_dir
                / f"{hashlib.md5(str(nb_full_path).encode()).hexdigest()}.json"
            )
            cache_data = self._read_cache(cache_file)

            md_full_path = self.docs_dir / md_path

            # Skip processing if source unchanged and output exists
            if (
                cache_data.get("source_hash") == source_hash
                and md_full_path.exists()
            ):
                logger.info(f"Skipping unchanged notebook: {nb_path}")

                # Register markdown file (let MkDocs handle it normally)
                self._register_file(files, md_path, config)

                # Register cached output files only if they don't exist
                nb_name = nb_full_path.stem
                output_dir_name = f"{nb_name}_files"
                for output_file_name in cache_data.get("output_files", []):
                    rel_img_path = str(Path(md_path).parent / output_file_name)
                    # Only register if file actually exists and not already registered
                    output_file_path = self.docs_dir / rel_img_path
                    if output_file_path.exists():
                        self._register_file(files, rel_img_path, config)

                continue

            logger.info(f"Processing notebook: {nb_path}")

            md_full_path.parent.mkdir(parents=True, exist_ok=True)

            # Read notebook once
            nb_node = (
                jupytext.read(nb_full_path)
                if nb_full_path.suffix == ".py"
                else nbformat.read(nb_full_path, as_version=4)
            )

            nb_name = nb_full_path.stem
            output_dir_name = f"{nb_name}_files"
            self.exporter.template.environment.globals["output_dir_name"] = (
                output_dir_name
            )

            body, resources = self.exporter.from_notebook_node(nb_node)

            output_files = []
            if "outputs" in resources:
                md_dir = md_full_path.parent
                output_dir = md_dir / output_dir_name
                output_dir.mkdir(parents=True, exist_ok=True)

                for name, data in resources["outputs"].items():
                    output_file_path = output_dir / name
                    output_file_path.write_bytes(data)

                    rel_img_path = str(
                        Path(md_path).parent / output_dir_name / name
                    )
                    output_files.append(f"{output_dir_name}/{name}")

                    # Remove old file reference and add new one
                    asset_file = files.get_file_from_path(rel_img_path)
                    if asset_file:
                        files.remove(asset_file)

                    self._register_file(files, rel_img_path, config)

            # Process includes
            included_files = include_pattern.findall(body)

            for included_file_path_in_md in included_files:
                rel_doc_path = (
                    Path(included_file_path_in_md[5:])
                    if included_file_path_in_md.startswith("docs/")
                    else Path(included_file_path_in_md)
                )

                dest_full_path = self.docs_dir / rel_doc_path
                dest_full_path.parent.mkdir(parents=True, exist_ok=True)

                source_full_path = self.root_dir / rel_doc_path

                if not source_full_path.exists():
                    logger.warning(
                        f"Included file not found at source: {source_full_path}"
                    )
                    continue

                try:
                    shutil.copy2(source_full_path, dest_full_path)
                except Exception as e:
                    logger.error(
                        f"Error copying included file {source_full_path}: {e}"
                    )

            # Write markdown file
            md_full_path.write_text(body, encoding="utf-8")

            # Update cache
            self._write_cache(
                cache_file,
                {
                    "source_hash": source_hash,
                    "output_files": output_files,
                },
            )

            # Register markdown file
            existing_file = files.get_file_from_path(md_path)
            if existing_file:
                files.remove(existing_file)

            self._register_file(files, md_path, config)

        return files

    def on_serve(self, server, config, **kwargs):
        logger.info("on_serve triggered")
        for _, nb_path in self.notebook_mappings.items():
            nb_full_path = self.root_dir / nb_path

            if not nb_full_path.exists():
                continue
            server.watch(path=str(nb_full_path))
        return server
