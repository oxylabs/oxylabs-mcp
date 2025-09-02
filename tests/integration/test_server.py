import json
import re
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import FastMCP
from httpx import HTTPStatusError, Request, RequestError, Response

from oxylabs_mcp.config import settings
from tests.integration import params


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        pytest.param(
            "universal_scraper",
            {"url": "test_url"},
            id="universal_scraper",
        ),
        pytest.param(
            "google_search_scraper",
            {"query": "Generic query"},
            id="google_search_scraper",
        ),
        pytest.param(
            "amazon_search_scraper",
            {"query": "Generic query"},
            id="amazon_search_scraper",
        ),
        pytest.param(
            "amazon_product_scraper",
            {"query": "Generic query"},
            id="amazon_product_scraper",
        ),
    ],
)
async def test_default_headers_are_set(
    mcp: FastMCP,
    request_data: Request,
    oxylabs_client: AsyncMock,
    tool: str,
    arguments: dict,
):
    mock_response = Response(
        200,
        content=json.dumps(params.STR_RESPONSE),
        request=request_data,
    )

    oxylabs_client.post.return_value = mock_response
    oxylabs_client.get.return_value = mock_response

    await mcp._call_tool(tool, arguments=arguments)

    assert "x-oxylabs-sdk" in oxylabs_client.context_manager_call_kwargs["headers"]

    oxylabs_sdk_header = oxylabs_client.context_manager_call_kwargs["headers"]["x-oxylabs-sdk"]
    client_info, _ = oxylabs_sdk_header.split(maxsplit=1)

    client_info_pattern = re.compile(r"oxylabs-mcp-fake_cursor/(\d+)\.(\d+)\.(\d+)$")
    assert re.match(client_info_pattern, client_info)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        pytest.param(
            "universal_scraper",
            {"url": "test_url"},
            id="universal_scraper",
        ),
        pytest.param(
            "google_search_scraper",
            {"query": "Generic query"},
            id="google_search_scraper",
        ),
        pytest.param(
            "amazon_search_scraper",
            {"query": "Generic query"},
            id="amazon_search_scraper",
        ),
        pytest.param(
            "amazon_product_scraper",
            {"query": "Generic query"},
            id="amazon_product_scraper",
        ),
    ],
)
@pytest.mark.parametrize(
    ("exception", "expected_text"),
    [
        pytest.param(
            HTTPStatusError(
                "HTTP status error",
                request=MagicMock(),
                response=MagicMock(status_code=500, text="Internal Server Error"),
            ),
            "HTTP error during POST request: 500 - Internal Server Error",
            id="https_status_error",
        ),
        pytest.param(
            RequestError("Request error"),
            "Request error during POST request: Request error",
            id="request_error",
        ),
        pytest.param(
            Exception("Unexpected exception"),
            "Error: Unexpected exception",
            id="unhandled_exception",
        ),
    ],
)
async def test_request_client_error_handling(
    mcp: FastMCP,
    request_data: Request,
    oxylabs_client: AsyncMock,
    tool: str,
    arguments: dict,
    exception: Exception,
    expected_text: str,
):
    oxylabs_client.post.side_effect = [exception]
    oxylabs_client.get.side_effect = [exception]

    result = await mcp._call_tool(tool, arguments=arguments)

    assert result.content[0].text == expected_text


@pytest.mark.parametrize("transport", ["stdio", "streamable-http"])
async def test_list_tools(mcp: FastMCP, transport: str):
    settings.MCP_TRANSPORT = transport
    tools = await mcp._mcp_list_tools()
    assert len(tools) == 10
