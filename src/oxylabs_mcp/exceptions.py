class MCPServerError(Exception):
    """Generic MCP server exception."""

    def stringify(self) -> str:
        """Convert the error to a readable string."""
        return str(self)
