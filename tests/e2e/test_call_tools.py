import os
from contextlib import asynccontextmanager

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@asynccontextmanager
async def get_oxylabs_mcp_client():
    server_params = StdioServerParameters(
        command="uv",  # Using uv to run the server
        args=["run", "oxylabs-mcp"],
        env={
            "OXYLABS_USERNAME": os.getenv("OXYLABS_USERNAME"),
            "OXYLABS_PASSWORD": os.getenv("OXYLABS_PASSWORD"),
        },
        cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("url", "min_response_len"),
    [
        (
            "https://maisonpur.com/best-non-toxic-cutting-boards-safer-options-for-a-healthy-kitchen/",
            10000,
        ),
        ("https://sandbox.oxylabs.io/products/1", 2500),
        ("https://sandbox.oxylabs.io/products/5", 3000),
    ],
)
async def test_universal_scraper_tool(url: str, min_response_len: int):
    async with get_oxylabs_mcp_client() as session:
        result = await session.call_tool("universal_scraper", arguments={"url": url})
        assert len(result.content[0].text) > min_response_len
