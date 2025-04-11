import json
from contextlib import nullcontext as does_not_raise
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from httpx import Request, Response
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools.base import ToolError
from mcp.types import TextContent

from oxylabs_mcp.server import mcp as mcp_server


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
        mock_response_data = {
            "results": [{"content": "<html><body>Mocked content</body></html>"}]
        }
        mock_response = Response(
            200, content=json.dumps(mock_response_data), request=request_data
        )

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
            patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)),
        ):
            result = await mcp.call_tool(
                "oxylabs_universal_scraper", arguments=arguments
            )
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
                        {
                            "results": [
                                {"content": "<html><body>Mocked content</body></html>"}
                            ]
                        }
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
            result = await mcp.call_tool(
                "oxylabs_universal_scraper", arguments=arguments
            )
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
            pytest.param(
                {"query": "Iphone 16"},
                does_not_raise(),
                {"results": [{"content": "Mocked content"}]},
                "Mocked content",
                id="query-only-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "parse": True},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="parse-enabled-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "render": "html"},
                does_not_raise(),
                {"results": [{"content": "Mocked content"}]},
                "Mocked content",
                id="render-enabled-args",
            ),
            *[
                pytest.param(
                    {"query": "Iphone 16", "user_agent_type": "mobile"},
                    does_not_raise(),
                    {"results": [{"content": "Mocked content"}]},
                    "Mocked content",
                    id=f"{uat}-user-agent-specified-args",
                )
                for uat in [
                    "desktop",
                    "desktop_chrome",
                    "desktop_firefox",
                    "desktop_safari",
                    "desktop_edge",
                    "desktop_opera",
                    "mobile",
                    "mobile_ios",
                    "mobile_android",
                    "tablet",
                ]
            ],
            pytest.param(
                {"query": "Iphone 16", "user_agent_type": "invalid"},
                pytest.raises(ToolError),
                {"results": [{"content": "Mocked content"}]},
                "Mocked content",
                id="invalid-user-agent-specified-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "start_page": 2},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="start-page-specified-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "start_page": -1},
                pytest.raises(ToolError),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="start-page-invalid-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "pages": 20},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="pages-specified-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "pages": -10},
                pytest.raises(ToolError),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="pages-invalid-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "limit": 100},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="limit-specified-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "limit": 0},
                pytest.raises(ToolError),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="limit-invalid-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "domain": "io"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="domain-specified-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "geo_location": "Miami, Florida"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
            pytest.param(
                {"query": "Iphone 16", "locale": "ja_JP"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
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
        mock_response = Response(
            200, content=json.dumps(response_data), request=request_data
        )

        oxylabs_client.post.return_value = mock_response

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
        ):
            result = await mcp.call_tool(
                "oxylabs_google_search_scraper", arguments=arguments
            )
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
        mock_response = Response(
            200, content=json.dumps('{"data": "value"}'), request=request_data
        )

        oxylabs_client.post.return_value = mock_response

        with (patch("os.environ", new=ENV_VARIABLES),):
            await mcp.call_tool("oxylabs_google_search_scraper", arguments=arguments)
            assert oxylabs_client.post.await_args.kwargs["json"] == expected_result

    # todo: think about the reuse of test params to achieve less code duplication
    @pytest.mark.parametrize(
        ("arguments", "expectation", "response_data", "expected_result"),
        [
            pytest.param(
                {"query": "Man's T-shirt"},
                does_not_raise(),
                {"results": [{"content": "Mocked content"}]},
                "Mocked content",
                id="query-only-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "parse": False},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '\n\n{"data": "value"}\n\n',
                id="parse-enabled-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "render": "html"},
                does_not_raise(),
                {"results": [{"content": "Mocked content"}]},
                "Mocked content",
                id="render-enabled-args",
            ),
            *[
                pytest.param(
                    {"query": "Man's T-shirt", "user_agent_type": "mobile"},
                    does_not_raise(),
                    {"results": [{"content": "Mocked content"}]},
                    "Mocked content",
                    id=f"{uat}-user-agent-specified-args",
                )
                for uat in [
                    "desktop",
                    "desktop_chrome",
                    "desktop_firefox",
                    "desktop_safari",
                    "desktop_edge",
                    "desktop_opera",
                    "mobile",
                    "mobile_ios",
                    "mobile_android",
                    "tablet",
                ]
            ],
            pytest.param(
                {"query": "Man's T-shirt", "user_agent_type": "invalid"},
                pytest.raises(ToolError),
                {"results": [{"content": "Mocked content"}]},
                "Mocked content",
                id="invalid-user-agent-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "start_page": 2},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="start-page-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "start_page": -1},
                pytest.raises(ToolError),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="start-page-invalid-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "pages": 20},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="pages-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "pages": -10},
                pytest.raises(ToolError),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="pages-invalid-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "domain": "io"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="domain-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "geo_location": "Miami, Florida"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "locale": "ja_JP"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "category_id": "QE21R9AV"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "merchant_id": "QE21R9AV"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
            pytest.param(
                {"query": "Man's T-shirt", "currency": "USD"},
                does_not_raise(),
                {"results": [{"content": '{"data": "value"}'}]},
                '{"data": "value"}',
                id="geo-location-specified-args",
            ),
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
        mock_response = Response(
            200, content=json.dumps(response_data), request=request_data
        )

        oxylabs_client.post.return_value = mock_response

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
        ):
            result = await mcp.call_tool(
                "oxylabs_amazon_search_scraper", arguments=arguments
            )
            assert result == [TextContent(type="text", text=expected_result)]
