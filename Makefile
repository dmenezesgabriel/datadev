jupyterlab:
	uv run --with jupyter jupyter lab

docs-dev:
	uv run -m mkdocs serve

tree:
	tree -L 5\
		 -I "node_modules" \
		 -I ".venv" \
		  -I ".git" \
		  -I ".mypy_cache" \
		  -I "dist" \
		  -a >> tree.txt
