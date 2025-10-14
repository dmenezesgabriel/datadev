"""
https://www.mkdocs.org/dev-guide/plugins/#events
"""

import hashlib
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
                if not ("data" in output and "text/html" in output["data"]):
                    continue
                html_content = "".join(output["data"]["text/html"])
                anchor_tag = "a"
                markdown_content = md(html_content, strip=[anchor_tag])
                output["data"]["text/markdown"] = markdown_content
                del output["data"]["text/html"]

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

    def on_config(self, config):
        logger.info("on_config triggered")
        self.root_dir = Path(self.config.get("root_dir")).resolve()
        self.docs_dir = Path(config["docs_dir"]).resolve()

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

            md_full_path = self.docs_dir / md_path
            md_full_path.parent.mkdir(parents=True, exist_ok=True)

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

            if not "outputs" in resources:
                continue
            md_dir = md_full_path.parent
            output_dir = md_dir / output_dir_name
            output_dir.mkdir(parents=True, exist_ok=True)

            for name, data in resources["outputs"].items():
                output_file_path = output_dir / name
                output_file_path.write_bytes(data)

                rel_img_path = str(
                    Path(md_path).parent / output_dir_name / name
                )

                asset_file = files.get_file_from_path(rel_img_path)
                if asset_file:
                    files.remove(asset_file)

                new_asset_file = File(
                    path=rel_img_path,
                    src_dir=str(self.docs_dir),
                    dest_dir=config["site_dir"],
                    use_directory_urls=config.get("use_directory_urls", True),
                )
                files.append(new_asset_file)

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
                    print(
                        f"Error copying included file {source_full_path}: {e}"
                    )

            new_hash = hashlib.md5(body.encode("utf-8")).hexdigest()
            existing_hash = None

            if md_full_path.exists():
                try:
                    existing_content = md_full_path.read_text(encoding="utf-8")
                    existing_hash = hashlib.md5(
                        existing_content.encode("utf-8")
                    ).hexdigest()
                except Exception:
                    existing_hash = None

            if new_hash != existing_hash:
                md_full_path.write_text(body, encoding="utf-8")

            existing_file = files.get_file_from_path(md_path)

            if existing_file:
                files.remove(existing_file)

            new_file = File(
                path=md_path,
                src_dir=str(self.docs_dir),
                dest_dir=config["site_dir"],
                use_directory_urls=config.get("use_directory_urls", True),
            )
            files.append(new_file)

        return files

    def on_serve(self, server, config, **kwargs):
        logger.info("on_serve triggered")
        for _, nb_path in self.notebook_mappings.items():
            nb_full_path = self.root_dir / nb_path

            if not nb_full_path.exists():
                continue
            server.watch(path=str(nb_full_path))
        return server
