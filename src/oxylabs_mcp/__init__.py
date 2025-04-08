from . import server


def main():
    """Start the MCP server."""
    server.main()


# Optionally expose other important items at package level
__all__ = ["main", "server"]
