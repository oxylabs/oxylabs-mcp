import json
from httpx import Request, Response
import pytest
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools.base import ToolError
from mcp.types import TextContent
from oxylabs_mcp.server import mcp as mcp_server
from contextlib import nullcontext as does_not_raise
from unittest.mock import AsyncMock, patch


ENV_VARIABLES = {'OXYLABS_USERNAME': 'test_user', 'OXYLABS_PASSWORD': 'test_pass'}


class TestMcpServer:
    @pytest.fixture
    def mcp(self) -> FastMCP:
        return mcp_server

    @pytest.fixture
    def request_data(self):
        return Request("POST", "https://example.com/v1/queries")

    @pytest.mark.parametrize(
        "arguments, expectation, expected_result",
        [
            pytest.param(
                {"url": "test_url"},
                does_not_raise(),
                "Mocked content",
                id="url-only-args"
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-enabled-args"
            ),
            pytest.param(
                {"url": "test_url", "parse": False},
                does_not_raise(),
                "Mocked content",
                id="parse-disabled-args"
            ),
            pytest.param(
                {"url": "test_url", "parse": "True"},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-enabled-passing-string-args"
            ),
            pytest.param(
                {"url": "test_url", "parse": True, "render": "html"},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-and-render-enabled-args"
            ),
            pytest.param(
                {"url": "test_url", "parse": True, "render": "None"},
                does_not_raise(),
                "<html><body>Mocked content</body></html>",
                id="parse-enabled-render-disabled-args"
            ),
            pytest.param(
                {"url": "test_url", "parse": True, "render": "png"},
                pytest.raises(ToolError),
                None,
                id="invalid-render-option-args"
            ),
            pytest.param(
                {},
                pytest.raises(ToolError),
                None,
                id="no-url-args"
            ),
        ]
    )
    @pytest.mark.asyncio
    async def test_oxylabs_scraper_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        expectation,
        expected_result: str
    ):
        mock_response_data = {
            "results": [{"content": "<html><body>Mocked content</body></html>"}]
        }
        mock_response = Response(
            200,
            content=json.dumps(mock_response_data),
            request=request_data)

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
            patch(
                "httpx.AsyncClient.post",
                new=AsyncMock(return_value=mock_response)
            )
        ):
            result = await mcp.call_tool("oxylabs_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        "arguments, expectation, expected_result",
        [
            pytest.param(
                {"url": "test_url"},
                does_not_raise(),
                "Mocked content",
                id="url-only-args"
            ),
            pytest.param(
                {"url": "test_url", "render": "html"},
                does_not_raise(),
                "Mocked content",
                id="render-enabled-args"
            ),
            pytest.param(
                {"url": "test_url", "render": "None"},
                does_not_raise(),
                "Mocked content",
                id="render-disabled-args"
            ),
            pytest.param(
                {"url": "test_url", "render": "png"},
                pytest.raises(ToolError),
                None,
                id="invalid-render-option-args"
            ),
            pytest.param(
                {},
                pytest.raises(ToolError),
                None,
                id="no-url-args"
            ),
        ]
    )
    @pytest.mark.asyncio
    async def test_oxylabs_web_unblocker_arguments(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        expectation,
        expected_result: str
    ):
        mock_response_data = "<html><body>Mocked content</body></html>"
        mock_response = Response(
            200,
            text=mock_response_data,
            request=request_data)

        with (
            expectation,
            patch("os.environ", new=ENV_VARIABLES),
            patch(
                "httpx.AsyncClient.get",
                new=AsyncMock(return_value=mock_response)
            )
        ):
            result = await mcp.call_tool("oxylabs_web_unblocker", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]

    @pytest.mark.parametrize(
        "arguments, response, expected_result",
        [
            pytest.param(
                {"url": "test_url"},
                Response(
                    200,
                    content=json.dumps(
                        {"results": [
                            {"content": "<html><body>Mocked content</body></html>"}
                        ]}
                    )
                ),
                "Mocked content",
                id="url-only-result"
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                Response(
                    200,
                    content=json.dumps(
                        {"results": [{"content": {"url": "test_url"}}]}
                    )
                ),
                "{'url': 'test_url'}",
                id="parse-enabled-result"
            ),
            pytest.param(
                {"url": "test_url", "parse": False},
                Response(
                    200,
                    content=json.dumps(
                        {"results": [
                            {"content": "<html><body>Mocked content</body></html>"}
                        ]}
                    )
                ),
                "Mocked content",
                id="parse-disabled-result"
            ),
            pytest.param(
                {"url": "test_url", "parse": True},
                Response(
                    403,
                    content=json.dumps({"message": "Unauthorized"})
                ),
                'HTTP error during POST request: 403 - {"message": "Unauthorized"}',
                id="403-unauthorized-result"
            )
        ]
    )
    @pytest.mark.asyncio
    async def test_oxylabs_scraper_results(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        response: Response,
        expected_result: str
    ):
        response.request = request_data
        with (
            patch("os.environ", new=ENV_VARIABLES),
            patch(
                "httpx.AsyncClient.post",
                new=AsyncMock(return_value=response)
            )
        ):
            result = await mcp.call_tool("oxylabs_scraper", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]


    @pytest.mark.parametrize(
        "arguments, response, expected_result",
        [
            pytest.param(
                {"url": "test_url"},
                Response(
                    200,
                    text="<html><body>Mocked content</body></html>"
                ),
                "Mocked content",
                id="url-only-result"
            ),
            pytest.param(
                {"url": "test_url", "render": "html"},
                Response(
                    200,
                    text="<html><body>Mocked content</body></html>",
                ),
                "Mocked content",
                id="parse-disabled-result"
            )
        ]
    )
    @pytest.mark.asyncio
    async def test_oxylabs_web_unblocker_results(
        self,
        mcp: FastMCP,
        request_data: Request,
        arguments: dict,
        response: Response,
        expected_result: str
    ):
        response.request = request_data
        with (
            patch("os.environ", new=ENV_VARIABLES),
            patch(
                "httpx.AsyncClient.get",
                new=AsyncMock(return_value=response)
            )
        ):
            result = await mcp.call_tool("oxylabs_web_unblocker", arguments=arguments)
            assert result == [TextContent(type="text", text=expected_result)]
