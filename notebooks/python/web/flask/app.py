# ---
# jupyter:
#   language_info:
#     name: python # <- for syntax highlighting purposes
# ---

# %% [markdown]
# # Flask
# Flask is a python web framework.

# %% [markdown]
# ## WSGI
# > Web Server Gateway Interface
#
# Is a protocol of communication used so the request from the webserver can
# reach the _web app_, in this case **Flask**.

# %% [markdown]
# ## Jinja 2
# It is a web template engine, that can combine templates with data sources.
# A data source can be for example:
#
# - CSV Sheet
# - SQL Database
# - NoSQL Database
# - Machine Learning model

# %% [markdown]
# Those below are astral/uv script dependencies, it can be define inside script
# file.
# You can run it like `uv run my_script.py` then they will be automatically
# installed

# %%
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "flask",
# ]
# ///


# %%
from flask import Flask, render_template

app = Flask(__name__)  # WSGI compliant application instance


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(
        debug=True,  # Enables hot reload if True
    )
