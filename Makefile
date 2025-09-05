docs-dev:
	uv run -m mkdocs serve

tree:
	tree -L 5 -I "node_modules" -I ".venv" -I ".git" -I ".mypy_cache" -I "dist" -I "udemy-angular-complete-guide" -I ".next" -a >> tree.txt