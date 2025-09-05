import hashlib
import os
from pathlib import Path

import html2text
import nbconvert
import nbformat
from markdownify import markdownify as md
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from nbconvert import MarkdownExporter


class MkDocsJupyterPlugin(BasePlugin):
    config_scheme = (
        ("root_dir", config_options.Type(str, default=".")),
        ("template_file", config_options.Type(str, default=None)),
    )

    def on_config(self, config):
        self.root_dir = Path(self.config.get("root_dir")).resolve()
        self.docs_dir = Path(config["docs_dir"]).resolve()

        template_file = self.config.get("template_file")

        # Get the path to nbconvert's built-in templates from the module's path
        nbconvert_templates_dir = (
            Path(os.path.dirname(nbconvert.__file__)) / "templates"
        )

        if template_file:
            # Resolve the full path to your custom template
            custom_template_path = Path(template_file).resolve()

            # The template_file argument should be the filename, and the directory
            # should be in extra_template_paths.
            self.exporter = MarkdownExporter(
                template_file=str(custom_template_path.name),
                extra_template_paths=[
                    str(custom_template_path.parent),
                    str(nbconvert_templates_dir),
                ],
            )
        else:
            self.exporter = MarkdownExporter()

        self.exporter.filters["markdownify"] = md
        # {%- block execute_result scoped -%}
        # {{ output.data.get('text/html', '') | markdownify -}}
        # {{ output.data.get('text/plain', '') }}
        # {%- endblock execute_result -%}

        self.notebook_mappings = {}

        def walk_nav(items):
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, list):
                            walk_nav(v)
                        elif isinstance(v, str) and v.endswith(".ipynb"):
                            md_path = str(Path(v).with_suffix(".md"))
                            self.notebook_mappings[md_path] = v
                            items[i][k] = md_path

        walk_nav(config["nav"])
        return config

    def on_files(self, files, config):
        for md_path, nb_path in self.notebook_mappings.items():
            nb_full_path = (self.root_dir / nb_path).resolve()
            if not nb_full_path.exists():
                print(
                    f"Warning: notebook {nb_path} not found at {nb_full_path}"
                )
                continue

            md_full_path = self.docs_dir / md_path
            md_full_path.parent.mkdir(parents=True, exist_ok=True)

            nb_node = nbformat.read(nb_full_path, as_version=4)

            nb_name = nb_full_path.stem
            output_dir_name = f"{nb_name}_files"
            self.exporter.template.environment.globals["output_dir_name"] = (
                output_dir_name
            )

            body, resources = self.exporter.from_notebook_node(nb_node)

            if "outputs" in resources:
                md_dir = md_full_path.parent
                output_dir = md_dir / output_dir_name
                output_dir.mkdir(parents=True, exist_ok=True)

                for name, data in resources["outputs"].items():
                    output_file_path = output_dir / name
                    output_file_path.write_bytes(data)

                    # Add the generated image file to MkDocs' file list.
                    # The path must be relative to the docs_dir and include the new subdirectory.
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
                server.watch(str(nb_full_path))
        return server
