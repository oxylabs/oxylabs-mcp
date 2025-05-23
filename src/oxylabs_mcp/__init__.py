from oxylabs_mcp.server import mcp


def main() -> None:
    """Start the MCP server."""
    mcp.run()


# Optionally expose other important items at package level
__all__ = ["main", "server"]
