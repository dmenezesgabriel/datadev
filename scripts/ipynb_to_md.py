from pathlib import Path

from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode

template = Path("templates/jupyter.md.j2")
notebook = Path("notebooks/python/data-analysis/altair.ipynb")
notebook_output = Path("tmp.md")
import nbformat

# Load notebook
with notebook.open() as f:
    nb = nbformat.read(f, as_version=4)

# Set up MarkdownExporter with template
exporter = MarkdownExporter(template_file=str(template))

# Export notebook to Markdown
body, resources = exporter.from_notebook_node(nb)

# Write output
with notebook_output.open("w") as f:
    f.write(body)
