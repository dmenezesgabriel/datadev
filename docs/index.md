# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

- `mkdocs new [dir-name]` - Create a new project.
- `mkdocs serve` - Start the live-reloading docs server.
- `mkdocs build` - Build the documentation site.
- `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

```py title="add_numbers.py" linenums="1" hl_lines="2"
# Function to add two numbers
def add_two_numbers(num1, num2):
    return num1 + num2

# Example usage
result = add_two_numbers(5, 3)
print('The sum is:', result)
```

## Content tabs

=== "Markdown"

    This is standard Markdown content.

=== "ReStructuredText"

    This is **ReStructuredText** content.

|            | setosa | versicolor | virginica |
| ---------- | ------ | ---------- | --------- |
| setosa     | 10     | 0          | 0         |
| versicolor | 0      | 9          | 0         |
| virginica  | 0      | 0          | 11        |
