import base64
import json
import re
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Client, FastMCP
from httpx import HTTPStatusError, Request, RequestError, Response

from oxylabs_mcp import utils
from oxylabs_mcp.config import settings
from tests.integration import params


def _basic_auth(username: str, password: str) -> str:
    return "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()


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

    await mcp.call_tool(tool, arguments=arguments)

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

    result = await mcp.call_tool(tool, arguments=arguments)

    assert result.content[0].text == expected_text


@pytest.mark.parametrize("transport", ["stdio", "streamable-http"])
async def test_list_tools(mcp: FastMCP, transport: str):
    settings.MCP_TRANSPORT = transport
    try:
        async with Client(mcp) as client:
            tools = await client.list_tools()
        assert len(tools) == 10
    finally:
        settings.MCP_TRANSPORT = "stdio"


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        pytest.param(
            {"authorization": _basic_auth("basic_user", "basic_pass")},
            ("basic_user", "basic_pass"),
            id="authorization_basic",
        ),
        pytest.param(
            {"x-oxylabs-username": "dash_user", "x-oxylabs-password": "dash_pass"},
            ("dash_user", "dash_pass"),
            id="documented_headers",
        ),
        pytest.param(
            {"oxylabs_username": "legacy_user", "oxylabs_password": "legacy_pass"},
            ("legacy_user", "legacy_pass"),
            id="legacy_underscore_headers",
        ),
        pytest.param(
            {
                "authorization": _basic_auth("basic_user", "basic_pass"),
                "x-oxylabs-username": "dash_user",
                "x-oxylabs-password": "dash_pass",
            },
            ("basic_user", "basic_pass"),
            id="authorization_basic_takes_priority",
        ),
        pytest.param(
            {"authorization": "Bearer some-token"},
            (None, None),
            id="non_basic_authorization_is_ignored",
        ),
        pytest.param(
            {"authorization": "Basic not-base64!"},
            (None, None),
            id="malformed_basic_credentials_are_ignored",
        ),
        pytest.param({}, (None, None), id="no_credentials"),
    ],
)
def test_get_oxylabs_auth_with_http_transport(request_context, headers, expected):
    settings.MCP_TRANSPORT = "streamable-http"
    try:
        request_context.request_context.request.headers = headers
        assert utils.get_oxylabs_auth() == expected
    finally:
        settings.MCP_TRANSPORT = "stdio"


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        pytest.param(
            {"x-oxylabs-ai-studio-api-key": "dash_key"},
            "dash_key",
            id="documented_header",
        ),
        pytest.param(
            {"oxylabs_ai_studio_api_key": "legacy_key"},
            "legacy_key",
            id="legacy_underscore_header",
        ),
        pytest.param({}, None, id="no_api_key"),
    ],
)
def test_get_oxylabs_ai_studio_api_key_with_http_transport(request_context, headers, expected):
    settings.MCP_TRANSPORT = "streamable-http"
    try:
        request_context.request_context.request.headers = headers
        assert utils.get_oxylabs_ai_studio_api_key() == expected
    finally:
        settings.MCP_TRANSPORT = "stdio"


@pytest.mark.asyncio
async def test_scraper_tool_without_credentials_returns_actionable_error(
    mcp: FastMCP,
    request_context,
    oxylabs_client: AsyncMock,
):
    settings.MCP_TRANSPORT = "streamable-http"
    try:
        request_context.request_context.request.headers = {}

        with pytest.raises(Exception, match="dashboard.oxylabs.io") as exc_info:
            await mcp.call_tool("universal_scraper", arguments={"url": "test_url"})

        assert "Authorization" in str(exc_info.value)
    finally:
        settings.MCP_TRANSPORT = "stdio"
