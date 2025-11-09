# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp==1.21.0",
#     "duckdb==1.4.1",
# ]
# ///

import argparse
from typing import Any

import duckdb  # type: ignore
from mcp.server.fastmcp import FastMCP  # type: ignore

mcp = FastMCP(
    name="DuckDB",
    host="0.0.0.0",
    port=8333,
    stateless_http=True,
)

DB_PATH = "database.duckdb"


def get_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(DB_PATH)


@mcp.tool()
def list_tables() -> list[dict[str, Any]]:
    """List all tables in the database"""
    with get_connection() as conn:
        result = conn.execute("SHOW TABLES").fetchall()
        return [{"name": row[0]} for row in result]


@mcp.tool()
def create_table(table_name: str, columns: str) -> str:
    """Create a new table. columns should be SQL column definitions like 'id INTEGER, name VARCHAR, amount DECIMAL(10,2)'"""
    with get_connection() as conn:
        conn.execute(f"CREATE TABLE {table_name} ({columns})")
        return f"Table {table_name} created"


@mcp.tool()
def insert_data(table_name: str, columns: str, values: str) -> str:
    """Insert data into table. columns like 'name, amount' and values like \"'Product A', 100.50\" """
    with get_connection() as conn:
        conn.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        return f"Data inserted into {table_name}"


@mcp.tool()
def query_data(sql: str) -> list[dict[str, Any]]:
    """Execute SELECT query and return results"""
    with get_connection() as conn:
        result = conn.execute(sql).fetchall()
        columns = [desc[0] for desc in conn.description]
        return [dict(zip(columns, row)) for row in result]


@mcp.tool()
def create_table_from_csv(table_name: str, csv_url: str) -> str:
    """Create a table from a CSV URL. csv_url should be an HTTP(S) URL to a CSV file"""
    with get_connection() as conn:
        conn.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM read_csv('{csv_url}')"
        )
        return f"Table {table_name} created from {csv_url}"


@mcp.tool()
def drop_table(table_name: str) -> str:
    """Drop a table from the database"""
    with get_connection() as conn:
        conn.execute(f"DROP TABLE {table_name}")
        return f"Table {table_name} dropped"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run MCP server with optional transport"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport method to use (default: stdio)",
    )
    args = parser.parse_args()

    print(f"Running server with {args.transport} transport")
    mcp.run(transport=args.transport)
