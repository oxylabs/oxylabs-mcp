import json
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import FastMCP
from httpx import Request, Response
from mcp.types import TextContent

from tests.integration import params
from tests.utils import convert_context_params, prepare_expected_arguments


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.URL_ONLY,
        params.NO_URL,
        params.RENDER_HTML_WITH_URL,
        params.RENDER_INVALID_WITH_URL,
        *params.USER_AGENTS_WITH_URL,
        params.GEO_LOCATION_SPECIFIED_WITH_URL,
    ],
)
@pytest.mark.asyncio
async def test_oxylabs_scraper_arguments(
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
        patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)),
    ):
        result = await mcp._call_tool("universal_scraper", arguments=arguments)

        assert oxylabs_client.post.call_args.kwargs == {
            "json": convert_context_params(prepare_expected_arguments(arguments)),
        }
        assert result.content == [TextContent(type="text", text=expected_result)]


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.QUERY_ONLY,
        params.PARSE_ENABLED,
        params.RENDER_HTML_WITH_QUERY,
        *params.USER_AGENTS_WITH_QUERY,
        *params.OUTPUT_FORMATS,
        params.INVALID_USER_AGENT,
        params.START_PAGE_SPECIFIED,
        params.PAGES_SPECIFIED,
        params.LIMIT_SPECIFIED,
        params.DOMAIN_SPECIFIED,
        params.GEO_LOCATION_SPECIFIED_WITH_QUERY,
        params.LOCALE_SPECIFIED,
    ],
)
@pytest.mark.asyncio
async def test_google_search_scraper_arguments(
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

    with expectation:
        result = await mcp._call_tool("google_search_scraper", arguments=arguments)

        assert oxylabs_client.post.call_args.kwargs == {
            "json": {
                "source": "google_search",
                "parse": True,
                **prepare_expected_arguments(arguments),
            }
        }
        assert result.content == [TextContent(type="text", text=expected_result)]


@pytest.mark.parametrize(
    ("ad_mode", "expected_result"),
    [
        (False, {"parse": True, "query": "Iphone 16", "source": "google_search"}),
        (True, {"parse": True, "query": "Iphone 16", "source": "google_ads"}),
    ],
)
@pytest.mark.asyncio
async def test_oxylabs_google_search_ad_mode_argument(
    mcp: FastMCP,
    request_data: Request,
    ad_mode: bool,
    expected_result: dict[str, Any],
    oxylabs_client: AsyncMock,
):
    arguments = {"query": "Iphone 16", "ad_mode": ad_mode}
    mock_response = Response(200, content=json.dumps('{"data": "value"}'), request=request_data)
    oxylabs_client.post.return_value = mock_response

    await mcp._call_tool("google_search_scraper", arguments=arguments)
    assert oxylabs_client.post.call_args.kwargs == {"json": expected_result}
    assert oxylabs_client.post.await_args.kwargs["json"] == expected_result


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.QUERY_ONLY,
        params.PARSE_ENABLED,
        params.RENDER_HTML_WITH_QUERY,
        *params.USER_AGENTS_WITH_QUERY,
        *params.OUTPUT_FORMATS,
        params.INVALID_USER_AGENT,
        params.START_PAGE_SPECIFIED,
        params.PAGES_SPECIFIED,
        params.DOMAIN_SPECIFIED,
        params.GEO_LOCATION_SPECIFIED_WITH_QUERY,
        params.LOCALE_SPECIFIED,
        params.CATEGORY_SPECIFIED,
        params.MERCHANT_ID_SPECIFIED,
        params.CURRENCY_SPECIFIED,
    ],
)
@pytest.mark.asyncio
async def test_amazon_search_scraper_arguments(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    request_context,
):
    mock_response = Response(200, content=json.dumps(response_data), request=request_data)
    oxylabs_client.post.return_value = mock_response

    with expectation:
        result = await mcp._call_tool("amazon_search_scraper", arguments=arguments)

        assert oxylabs_client.post.call_args.kwargs == {
            "json": {
                "source": "amazon_search",
                "parse": True,
                **convert_context_params(prepare_expected_arguments(arguments)),
            }
        }
        assert result.content == [TextContent(type="text", text=expected_result)]


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.QUERY_ONLY,
        params.PARSE_ENABLED,
        params.RENDER_HTML_WITH_QUERY,
        *params.USER_AGENTS_WITH_QUERY,
        *params.OUTPUT_FORMATS,
        params.INVALID_USER_AGENT,
        params.DOMAIN_SPECIFIED,
        params.GEO_LOCATION_SPECIFIED_WITH_QUERY,
        params.LOCALE_SPECIFIED,
        params.CURRENCY_SPECIFIED,
        params.AUTOSELECT_VARIANT_ENABLED,
    ],
)
@pytest.mark.asyncio
async def test_amazon_product_scraper_arguments(
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

    with expectation:
        result = await mcp._call_tool("amazon_product_scraper", arguments=arguments)

        assert oxylabs_client.post.call_args.kwargs == {
            "json": {
                "source": "amazon_product",
                "parse": True,
                **convert_context_params(prepare_expected_arguments(arguments)),
            }
        }
        assert result.content == [TextContent(type="text", text=expected_result)]
