# ---
# jupyter:
#   language_info:
#     name: python # <- for syntax highlighting purposes
# ---

# %% [markdown]
# # Flask


# %%
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "flask",
# ]
# ///


# %% [markdown]
# Application definition


# %%
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)  # WSGI compliant application instance


todos = [
    {"id": 1, "title": "task 1", "description": "task 1"},
    {"id": 2, "title": "task 1", "description": "task 1"},
]

# %% [markdown]
# Retrieve todos


# %%
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)


# %% [markdown]
# Retrieve todo by id


# %%
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_item(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "Todo Not Found"})
    return jsonify(todo)


# %% [markdown]
# Create a todo


# %%
@app.route("/todos", methods=["POST"])
def create_todo():
    if not request.json or not "title" in request.json:
        return jsonify({"error": "Todo must contain a title"})
    new_item = {
        "id": todos[-1]["id"] + 1 if todos else 1,
        "title": request.json["title"],
        "description": request.json["description"],
    }
    todos.append(new_item)
    return jsonify(new_item)


# %% [markdown]
# Update a todo


# %%
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "Todo Not Found"})

    todo["title"] = request.json.get("title", todo["title"])
    todo["description"] = request.json.get("description", todo["description"])
    return jsonify(todo)


# %% [markdown]
# Update a todo


# %%
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"message": "Todo deleted"})


# %% [markdown]
# Health route


# %%
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


# %% [markdown]
# Run the application


# %%

if __name__ == "__main__":
    app.run(
        debug=True,  # Enables hot reload if True
    )
