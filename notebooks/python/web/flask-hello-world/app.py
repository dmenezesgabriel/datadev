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
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)  # WSGI compliant application instance

# %% [markdown]
# We can also serve html templates:
# ```html title='templates/index.html'
# --8<-- "docs/notebooks/python/web/flask/templates/index.html"
# ```

# %% [markdown]
# Is needed to define the route that will serve the template:


# %%
@app.route("/")
def home():
    return render_template("index.html")  # root_dir/templates/index.html


# %% [markdown]
# GET Route


# %%
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


# %% [markdown]
# We can receive inputs from the UI
# ```html title='templates/form.html'
# --8<-- "docs/notebooks/python/web/flask/templates/form.html"
# ```

# %% [markdown]
# The inputs come from _verbs_ like **POST**, **PUT** and **PATCH**


# %%
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        return f"Hello {name} !"
    return render_template("form.html")


# %% [markdown]
# Dynamic template
#
# Jinja2 Templating engine
#
# - `{{ }}`: Expressions
# - `{%...%}`: Conditions
# - `{#...#}`: Comments
#
# ```html title='templates/result.html'
# --8<-- "docs/notebooks/python/web/flask/templates/result.html"
# ```

# %% [markdown]
# Route with params


# %%
@app.route("/success/<int:score>")
def success(score):
    return render_template("result.html", result=score)


# %% [markdown]
# Running the application


# %%

if __name__ == "__main__":
    app.run(
        debug=True,  # Enables hot reload if True
    )
