import re
from pathlib import Path
from typing import Any, Dict, List

from markdownify import markdownify as md  # type: ignore
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode


class HtmlOutputToMarkdownProcessor(Preprocessor):

    def preprocess_cell(
        self, cell: NotebookNode, resources: Dict[str, Any], index: int
    ) -> tuple[NotebookNode, Dict[str, Any]]:
        if cell.cell_type == "code" and cell.get("outputs"):
            for output in cell.outputs:

                if output.output_type == "stream":
                    output["text"] = output.get("text", [])

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
                ):
                    plain_text = "".join(output["data"]["text/plain"])
                    fenced_code_block = f"``` linenums='0'\n{plain_text}\n```"
                    output["data"]["text/markdown"] = fenced_code_block

                if (
                    "data" in output
                    and "application/vnd.vegalite.v5+json" in output["data"]
                ):
                    json_content = output["data"][
                        "application/vnd.vegalite.v5+json"
                    ]
                    markdown_content = (
                        f"```vegalite linenums='0'\n{json_content}\n```"
                    )
                    output["data"]["text/markdown"] = markdown_content
                    del output["data"]["application/vnd.vegalite.v5+json"]

                elif (
                    "data" in output
                    and "image/png" in output["data"]
                    and "metadata" in output
                    and "filenames" in output["metadata"]
                    and "image/png" in output["metadata"]["filenames"]
                ):
                    filename = output["metadata"]["filenames"]["image/png"]
                    image_markdown = f"![{filename}]({filename})"
                    output["data"]["text/markdown"] = image_markdown

        return cell, resources


template = Path("templates/jupyter.md.j2")
notebook = Path("scripts/test.ipynb")
notebook_output = Path("tmp.md")
import nbformat

# Load notebook
with notebook.open() as f:
    nb = nbformat.read(f, as_version=4)

preprocessors_list = [HtmlOutputToMarkdownProcessor]
exporter = MarkdownExporter(
    template_file=str(template),
    preprocessors=preprocessors_list,
)

# Export notebook to Markdown
body, resources = exporter.from_notebook_node(nb)

print(body)

# Write output
# with notebook_output.open("w") as f:
#     f.write(body)
