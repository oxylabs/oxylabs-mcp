from fastmcp.server.dependencies import get_context


class MCPServerError(Exception):
    """Generic MCP server exception."""

    async def process(self) -> str:
        """Process exception."""
        err = str(self)
        await get_context().error(err)
        return err
