from pathlib import Path
from typing import Any, Dict

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
                if not ("data" in output and "text/html" in output["data"]):
                    continue
                html_content = "".join(output["data"]["text/html"])
                anchor_tag = "a"
                markdown_content = md(html_content, strip=[anchor_tag])
                output["data"]["text/markdown"] = markdown_content
                del output["data"]["text/html"]

        return cell, resources


template = Path("templates/jupyter.md.j2")
notebook = Path("notebooks/python/data-analysis/pandas.ipynb")
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

# Write output
with notebook_output.open("w") as f:
    f.write(body)
