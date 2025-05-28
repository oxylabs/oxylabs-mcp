from mcp.server.fastmcp import Context


class MCPServerError(Exception):
    """Generic MCP server exception."""

    async def process(self, ctx: Context) -> str:  # type: ignore[type-arg]
        """Process exception."""
        err = str(self)
        await ctx.error(err)
        return err
