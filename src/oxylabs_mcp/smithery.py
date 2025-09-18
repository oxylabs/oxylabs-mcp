from fastmcp import FastMCP
from smithery.decorators import smithery

from oxylabs_mcp import mcp


@smithery.server()
def get_smithery_server() -> FastMCP:
    """Create Smithery server."""
    return mcp
