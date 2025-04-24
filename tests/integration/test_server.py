import json
import re
from contextlib import nullcontext as does_not_raise
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import Request, Response
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools.base import ToolError
from mcp.types import TextContent

from oxylabs_mcp.server import mcp as mcp_server
from tests.integration import params


ENV_VARIABLES = {"OXYLABS_USERNAME": "test_user", "OXYLABS_PASSWORD": "test_pass"}


class TestMcpServer:
    @pytest.fixture
    def mcp(self) -> FastMCP:
        return mcp_server

    @pytest.fixture
    def request_data(self):
        return Request("POST", "https://example.com/v1/queries")

    @pytest.mark.parametrize(
        ("arguments", "expectation", "expected_result"),
        [
            pytest.param(
                {"url": "test_url"},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="url-only-args",
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-enabled-args",
            ),
            pytest.param(
                {"url": "test_url", "parse": False},
                does_not_raise(),
                "Mocked content",
                id="parse-disabled-args",
            ),
            pytest.param(
                {"url": "test_url", "parse": "True"},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-enabled-passing-string-args",
            ),
            pytest.param(
                {"url": "test_url", "parse": True, "render": "html"},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-and-render-enabled-args",
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-enabled-render-disabled-args",
            ),
            pytest.param(
                {"url": "test_url", "parse": True, "render": "png"},
                pytest.raises(ToolError),
                None,
                id="invalid-render-option-args",
            ),
            pytest.param({}, pytest.raises(ToolError), None, id="no-url-args"),
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_scraper_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        expectation,
        expected_result: str,
    ):
        mock_response_data = {"results": [{"content": "<html><body>Mocked content</body></html>"}]}
        mock_response = Response(200, content=json.dumps(mock_response_data), request=request_data)

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
            patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)),
        ):
            result = await mcp.call_tool("oxylabs_universal_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        ("arguments", "expectation", "expected_result"),
        [
            pytest.param(
                {"url": "test_url"},
                does_not_raise(),
                "Mocked content",
                id="url-only-args",
            ),
            pytest.param(
                {"url": "test_url", "render": "html"},
                does_not_raise(),
                "Mocked content",
                id="render-enabled-args",
            ),
            pytest.param(
                {"url": "test_url"},
                does_not_raise(),
                "Mocked content",
                id="render-disabled-args",
            ),
            pytest.param(
                {"url": "test_url", "render": "png"},
                pytest.raises(ToolError),
                None,
                id="invalid-render-option-args",
            ),
            pytest.param({}, pytest.raises(ToolError), None, id="no-url-args"),
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_web_unblocker_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        expectation,
        expected_result: str,
    ):
        mock_response_data = "<html><body>Mocked content</body></html>"
        mock_response = Response(200, text=mock_response_data, request=request_data)

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
            patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)),
        ):
            result = await mcp.call_tool("oxylabs_web_unblocker", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        ("arguments", "response", "expected_result"),
        [
            pytest.param(
                {"url": "test_url"},
                Response(
                    200,
                    content=json.dumps({"results": [{"content": "Mocked content"}]}),
                ),
                "Mocked content",
                id="url-only-result",
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                Response(
                    200,
                    content=json.dumps({"results": [{"content": {"url": "test_url"}}]}),
                ),
                '{"url": "test_url"}',
                id="parse-enabled-result",
            ),
            pytest.param(
                {"url": "test_url", "parse": False},
                Response(
                    200,
                    content=json.dumps(
                        {"results": [{"content": "<html><body>Mocked content</body></html>"}]}
                    ),
                ),
                "Mocked content",
                id="parse-disabled-result",
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                Response(403, content=json.dumps({"message": "Unauthorized"})),
                'HTTP error during POST request: 403 - {"message": "Unauthorized"}',
                id="403-unauthorized-result",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_scraper_results(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        response: Response,
        expected_result: str,
        oxylabs_client: AsyncMock,
    ):
        response.request = request_data
        oxylabs_client.post.return_value = response

        with (patch("os.environ", new=ENV_VARIABLES),):
            result = await mcp.call_tool("oxylabs_universal_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        ("arguments", "response", "expected_result"),
        [
            pytest.param(
                {"url": "test_url"},
                Response(200, text="<html><body>Mocked content</body></html>"),
                "Mocked content",
                id="url-only-result",
            ),
            pytest.param(
                {"url": "test_url", "render": "html"},
                Response(
                    200,
                    text="<html><body>Mocked content</body></html>",
                ),
                "Mocked content",
                id="parse-disabled-result",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_web_unblocker_results(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        response: Response,
        expected_result: str,
        oxylabs_client: AsyncMock,
    ):
        response.request = request_data
        oxylabs_client.get.return_value = response

        with (patch("os.environ", new=ENV_VARIABLES),):
            result = await mcp.call_tool("oxylabs_web_unblocker", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        ("arguments", "expectation", "response_data", "expected_result"),
        [
            params.QUERY_ONLY,
            params.PARSE_ENABLED,
            params.RENDER_HTML,
            *params.USER_AGENTS,
            params.INVALID_USER_AGENT,
            params.START_PAGE_SPECIFIED,
            params.PAGES_SPECIFIED,
            params.LIMIT_SPECIFIED,
            params.DOMAIN_SPECIFIED,
            params.GEO_LOCATION_SPECIFIED,
            params.LOCALE_SPECIFIED,
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_google_search_scraper_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        response_data: str,
        arguments: dict,
        expectation,
        expected_result: str,
        oxylabs_client: AsyncMock,
    ):
        mock_response = Response(200, content=json.dumps(response_data), request=request_data)

        oxylabs_client.post.return_value = mock_response

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
        ):
            result = await mcp.call_tool("oxylabs_google_search_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        ("ad_mode", "expected_result"),
        [
            (False, {"parse": True, "query": "Iphone 16", "source": "google_search"}),
            (True, {"parse": True, "query": "Iphone 16", "source": "google_ads"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_google_search_ad_mode_argument(
        self,
        mcp: FastMCP,
        request_data: Request,
        ad_mode: bool,
        expected_result: dict[str, Any],
        oxylabs_client: AsyncMock,
    ):
        arguments = {"query": "Iphone 16", "ad_mode": ad_mode}
        mock_response = Response(200, content=json.dumps('{"data": "value"}'), request=request_data)

        oxylabs_client.post.return_value = mock_response

        with (patch("os.environ", new=ENV_VARIABLES),):
            await mcp.call_tool("oxylabs_google_search_scraper", arguments=arguments)
            assert oxylabs_client.post.await_args.kwargs["json"] == expected_result

    @pytest.mark.parametrize(
        ("arguments", "expectation", "response_data", "expected_result"),
        [
            params.QUERY_ONLY,
            params.PARSE_ENABLED,
            params.RENDER_HTML,
            *params.USER_AGENTS,
            params.INVALID_USER_AGENT,
            params.START_PAGE_SPECIFIED,
            params.PAGES_SPECIFIED,
            params.DOMAIN_SPECIFIED,
            params.GEO_LOCATION_SPECIFIED,
            params.LOCALE_SPECIFIED,
            params.CATEGORY_SPECIFIED,
            params.MERCHANT_ID_SPECIFIED,
            params.CURRENCY_SPECIFIED,
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_amazon_search_scraper_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        response_data: str,
        arguments: dict,
        expectation,
        expected_result: str,
        oxylabs_client: AsyncMock,
    ):
        mock_response = Response(200, content=json.dumps(response_data), request=request_data)

        oxylabs_client.post.return_value = mock_response

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
        ):
            result = await mcp.call_tool("oxylabs_amazon_search_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        ("arguments", "expectation", "response_data", "expected_result"),
        [
            params.QUERY_ONLY,
            params.PARSE_ENABLED,
            params.RENDER_HTML,
            *params.USER_AGENTS,
            params.INVALID_USER_AGENT,
            params.DOMAIN_SPECIFIED,
            params.GEO_LOCATION_SPECIFIED,
            params.LOCALE_SPECIFIED,
            params.CURRENCY_SPECIFIED,
            params.AUTOSELECT_VARIANT_ENABLED,
        ],
    )
    @pytest.mark.asyncio
    async def test_oxylabs_amazon_product_scraper_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        response_data: str,
        arguments: dict,
        expectation,
        expected_result: str,
        oxylabs_client: AsyncMock,
    ):
        mock_response = Response(200, content=json.dumps(response_data), request=request_data)

        oxylabs_client.post.return_value = mock_response

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
        ):
            result = await mcp.call_tool("oxylabs_amazon_product_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("tool", "arguments"),
        [
            pytest.param(
                "oxylabs_universal_scraper", {"url": "test_url"}, id="oxylabs_universal_scraper"
            ),
            pytest.param("oxylabs_web_unblocker", {"url": "test_url"}, id="oxylabs_web_unblocker"),
            pytest.param(
                "oxylabs_google_search_scraper",
                {"query": "Generic query"},
                id="oxylabs_google_search_scraper",
            ),
            pytest.param(
                "oxylabs_amazon_search_scraper",
                {"query": "Generic query"},
                id="oxylabs_amazon_search_scraper",
            ),
            pytest.param(
                "oxylabs_amazon_product_scraper",
                {"query": "Generic query"},
                id="oxylabs_amazon_product_scraper",
            ),
        ],
    )
    async def test_default_headers_are_set(
        self,
        mcp: FastMCP,
        request_data: Request,
        oxylabs_client: AsyncMock,
        request_session: MagicMock,
        tool: str,
        arguments: dict,
    ):
        request_session.client_params.clientInfo.name = "fake_cursor"

        mock_response = Response(
            200,
            content=json.dumps({"results": [{"content": "Mocked content"}]}),
            request=request_data,
        )

        oxylabs_client.post.return_value = mock_response
        oxylabs_client.get.return_value = mock_response

        with patch("os.environ", new=ENV_VARIABLES):
            await mcp.call_tool(tool, arguments=arguments)

        assert "x-oxylabs-sdk" in oxylabs_client.context_manager_call_kwargs["headers"]

        oxylabs_sdk_header = oxylabs_client.context_manager_call_kwargs["headers"]["x-oxylabs-sdk"]
        client_info, _ = oxylabs_sdk_header.split(maxsplit=1)

        client_info_pattern = re.compile(r"oxylabs-mcp-fake_cursor/(\d+)\.(\d+)\.(\d+)$")
        assert re.match(client_info_pattern, client_info)
