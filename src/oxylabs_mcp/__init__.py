import logging

from fastmcp import Context, FastMCP
from mcp import Tool as MCPTool

from oxylabs_mcp.config import settings
from oxylabs_mcp.tools.ai_studio import AI_TOOLS
from oxylabs_mcp.tools.ai_studio import mcp as ai_studio_mcp
from oxylabs_mcp.tools.scraper import SCRAPER_TOOLS
from oxylabs_mcp.tools.scraper import mcp as scraper_mcp
from oxylabs_mcp.utils import get_oxylabs_ai_studio_api_key, get_oxylabs_auth


class OxylabsMCPServer(FastMCP):
    """Oxylabs MCP server."""

    async def _mcp_list_tools(self) -> list[MCPTool]:
        """List all available Oxylabs tools."""
        async with Context(fastmcp=self):
            tools = await self._list_tools()

            username, password = get_oxylabs_auth()
            if not username or not password:
                tools = [tool for tool in tools if tool.name not in SCRAPER_TOOLS]

            if not get_oxylabs_ai_studio_api_key():
                tools = [tool for tool in tools if tool.name not in AI_TOOLS]

            return [
                tool.to_mcp_tool(
                    name=tool.key,
                    include_fastmcp_meta=self.include_fastmcp_meta,
                )
                for tool in tools
            ]


mcp = OxylabsMCPServer("oxylabs_mcp")

mcp.mount(ai_studio_mcp)
mcp.mount(scraper_mcp)


def main() -> None:
    """Start the MCP server."""
    logging.getLogger("oxylabs_mcp").setLevel(settings.LOG_LEVEL)

    params = {}

    if settings.MCP_TRANSPORT == "streamable-http":
        params["host"] = settings.MCP_HOST
        params["port"] = settings.MCP_PORT  # type: ignore[assignment]
        params["log_level"] = settings.LOG_LEVEL

    mcp.run(
        settings.MCP_TRANSPORT,
        **params,  # type: ignore[arg-type]
    )


# Optionally expose other important items at package level
__all__ = ["main"]
