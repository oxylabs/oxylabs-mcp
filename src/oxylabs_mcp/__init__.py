from oxylabs_mcp.server import add_tools, mcp


def main() -> None:
    """Start the MCP server."""
    add_tools(mcp)
    mcp.run()


# Optionally expose other important items at package level
__all__ = ["main", "server"]
