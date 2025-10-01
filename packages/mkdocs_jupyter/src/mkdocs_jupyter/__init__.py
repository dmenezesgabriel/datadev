import hashlib
import os
import re
import shutil
from pathlib import Path

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


class HtmlOutputToMarkdownProcessor(Preprocessor):

    def preprocess_cell(self, cell: NotebookNode, resources: dict, index: int):
        if cell.cell_type == "code" and "outputs" in cell:
            for output in cell.outputs:
                if "data" in output and "text/html" in output["data"]:
                    html_content = "".join(output["data"]["text/html"])
                    # Use markdownify to convert HTML output to Markdown
                    markdown_content = md(html_content, strip=["a"])
                    output["data"]["text/markdown"] = markdown_content
                    del output["data"]["text/html"]
        return cell, resources


class MkDocsJupyterPlugin(BasePlugin):
    config_scheme = (
        ("root_dir", config_options.Type(str, default=".")),
        ("template_file", config_options.Type(str, default=None)),
    )

    def on_config(self, config):
        self.root_dir = Path(self.config.get("root_dir")).resolve()
        self.docs_dir = Path(config["docs_dir"]).resolve()

        template_file = self.config.get("template_file")

        nbconvert_templates_dir = (
            Path(os.path.dirname(nbconvert.__file__)) / "templates"
        )
        preprocessors_list = [HtmlOutputToMarkdownProcessor]

        if template_file:
            custom_template_path = Path(template_file).resolve()
            self.exporter = MarkdownExporter(
                template_file=str(custom_template_path.name),
                extra_template_paths=[
                    str(custom_template_path.parent),
                    str(nbconvert_templates_dir),
                ],
                preprocessors=preprocessors_list,
            )
        else:
            self.exporter = MarkdownExporter(preprocessors=preprocessors_list)

        self.notebook_mappings = {}

        def walk_nav(items):
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, list):
                            walk_nav(v)
                        # Check for both .ipynb and .py files
                        elif isinstance(v, str) and (
                            v.endswith(".ipynb") or v.endswith(".py")
                        ):
                            # The target Markdown file path is always the original path with .md extension
                            md_path = str(Path(v).with_suffix(".md"))
                            # Map the resulting .md path back to the original .ipynb or .py file
                            self.notebook_mappings[md_path] = v
                            # Update the nav item to point to the .md file
                            items[i][k] = md_path

        walk_nav(config["nav"])
        return config

    def on_files(self, files, config):
        # Regex to find the MkDocs include syntax: --8<-- "path/to/file"
        # Captures the path inside the quotes
        include_pattern = re.compile(r'--8<--\s*["\']([^"\']+)["\']')

        for md_path, nb_path in self.notebook_mappings.items():
            nb_full_path = (self.root_dir / nb_path).resolve()
            if not nb_full_path.exists():
                print(
                    f"Warning: notebook/jupytext file {nb_path} not found at {nb_full_path}"
                )
                continue

            md_full_path = self.docs_dir / md_path
            md_full_path.parent.mkdir(parents=True, exist_ok=True)

            # --- Jupytext/Notebook reading logic ---
            if nb_full_path.suffix == ".py":
                nb_node = jupytext.read(nb_full_path)
            else:
                nb_node = nbformat.read(nb_full_path, as_version=4)

            nb_name = nb_full_path.stem
            output_dir_name = f"{nb_name}_files"
            self.exporter.template.environment.globals["output_dir_name"] = (
                output_dir_name
            )

            body, resources = self.exporter.from_notebook_node(nb_node)

            # --- Existing Image/Output copying logic ---
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

                    files.append(
                        File(
                            path=rel_img_path,
                            src_dir=str(self.docs_dir),
                            dest_dir=config["site_dir"],
                            use_directory_urls=config.get(
                                "use_directory_urls", True
                            ),
                        )
                    )
            # --- End of Existing Image/Output copying logic ---

            # --- New File Include Copying Logic Start ---
            included_files = include_pattern.findall(body)

            for included_file_path_in_md in included_files:
                # 1. Determine the path relative to the docs_dir
                # If path starts with "docs/", strip it, otherwise use as is.
                if included_file_path_in_md.startswith("docs/"):
                    # Use Path() to handle potential mixed slashes and OS differences
                    rel_doc_path = Path(included_file_path_in_md[5:])
                else:
                    rel_doc_path = Path(included_file_path_in_md)

                # 2. Determine the full *destination* path inside the docs_dir
                dest_full_path = self.docs_dir / rel_doc_path
                dest_full_path.parent.mkdir(parents=True, exist_ok=True)

                # 3. Determine the full *source* path (relative to self.root_dir)
                # Assumes the source file is located at the same path (relative to root_dir)
                # as the path inside docs_dir (after stripping 'docs/').
                source_full_path = self.root_dir / rel_doc_path

                if source_full_path.exists():
                    try:
                        # Copy the file to the docs_dir structure
                        shutil.copy2(source_full_path, dest_full_path)

                        # Add the copied file to MkDocs files list
                        # The path must be relative to the docs_dir
                        files.append(
                            File(
                                path=str(rel_doc_path),
                                src_dir=str(self.docs_dir),
                                dest_dir=config["site_dir"],
                                use_directory_urls=config.get(
                                    "use_directory_urls", True
                                ),
                            )
                        )
                        # Optional: Add a print statement for debugging
                        # print(f"Copied included file: {rel_doc_path}")

                    except Exception as e:
                        print(
                            f"Error copying included file {source_full_path}: {e}"
                        )
                else:
                    print(
                        f"Warning: Included file not found at source: {source_full_path}"
                    )
            # --- New File Include Copying Logic End ---

            # --- Rest of the existing logic (hashing, writing body, appending file) ---
            new_hash = hashlib.md5(body.encode("utf-8")).hexdigest()
            existing_hash = None
            if md_full_path.exists():
                with open(md_full_path, "r", encoding="utf-8") as f:
                    existing_content = f.read()
                    existing_hash = hashlib.md5(
                        existing_content.encode("utf-8")
                    ).hexdigest()

            if new_hash != existing_hash:
                md_full_path.write_text(body, encoding="utf-8")

            existing_file = None
            for f in files:
                if f.src_path == md_path:
                    existing_file = f
                    break

            if not existing_file:
                files.append(
                    File(
                        path=md_path,
                        src_dir=str(self.docs_dir),
                        dest_dir=config["site_dir"],
                        use_directory_urls=config.get(
                            "use_directory_urls", True
                        ),
                    )
                )

        return files

    def on_serve(self, server, config, **kwargs):
        for md_path, nb_path in self.notebook_mappings.items():
            nb_full_path = self.root_dir / nb_path
            if nb_full_path.exists():
                # Watch both .ipynb and .py files
                server.watch(str(nb_full_path))
        return server
