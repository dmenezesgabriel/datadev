# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp==1.21.0",
# ]
# ///

import argparse
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP  # type: ignore

mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # Only used for SSE transport (localhost)
    port=8333,  # Only used for SSE transport (set this to any port)
    stateless_http=True,
)


@mcp.tool()
def add(x: int, y: int) -> int:
    """Sum two integer numbers"""
    return x + y


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
