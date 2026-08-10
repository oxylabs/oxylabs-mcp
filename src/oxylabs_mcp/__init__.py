import logging
from typing import Any

from fastmcp import FastMCP

from oxylabs_mcp.config import settings
from oxylabs_mcp.tools.ai_studio import mcp as ai_studio_mcp
from oxylabs_mcp.tools.scraper import mcp as scraper_mcp


mcp = FastMCP("oxylabs_mcp")

mcp.mount(ai_studio_mcp)
mcp.mount(scraper_mcp)


def main() -> None:
    """Start the MCP server."""
    logging.getLogger("oxylabs_mcp").setLevel(settings.LOG_LEVEL)

    params: dict[str, Any] = {}

    if settings.MCP_TRANSPORT == "streamable-http":
        params["host"] = settings.MCP_HOST
        params["port"] = settings.PORT or settings.MCP_PORT
        params["log_level"] = settings.LOG_LEVEL
        params["stateless_http"] = settings.MCP_STATELESS_HTTP

    mcp.run(
        settings.MCP_TRANSPORT,
        **params,
    )


# Optionally expose other important items at package level
__all__ = ["main", "mcp"]
