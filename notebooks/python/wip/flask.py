# ---
# jupyter:
#   language_info:
#     name: python # <- for syntax highlighting purposes
# ---

# %% [markdown]
# Those are astral/uv script dependencies.
# You can run it like `uv run my_script.py` then they will be automatically
# installed

# %%
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "flask",
# ]
# ///

# %% [markdown]
# This is a markdown cell


# %%
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello</p>"


if __name__ == "__main__":
    app.run()
