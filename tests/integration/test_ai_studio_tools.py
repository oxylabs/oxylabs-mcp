import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import FastMCP
from httpx import Request
from mcp.types import TextContent
from oxylabs_ai_studio.apps.ai_search import AiSearchJob, SearchResult

from tests.integration import params
from tests.integration.params import SimpleSchema


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.AI_STUDIO_URL_ONLY,
        params.AI_STUDIO_URL_AND_OUTPUT_FORMAT,
        params.AI_STUDIO_URL_AND_SCHEMA,
        params.AI_STUDIO_URL_AND_RENDER_JAVASCRIPT,
        params.AI_STUDIO_URL_AND_RETURN_SOURCES_LIMIT,
        params.AI_STUDIO_URL_AND_GEO_LOCATION,
    ],
)
@pytest.mark.asyncio
async def test_ai_crawler(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    ai_crawler: AsyncMock,
):
    mock_result = MagicMock()
    mock_result.data = expected_result
    ai_crawler.crawl_async = AsyncMock(return_value=mock_result)

    arguments = {"user_prompt": "Scrape price and title", **arguments}

    with expectation:
        result = await mcp._call_tool("ai_crawler", arguments=arguments)

        assert result.content == [
            TextContent(type="text", text=json.dumps({"data": expected_result}))
        ]

        default_args = {
            "geo_location": None,
            "output_format": "markdown",
            "render_javascript": False,
            "return_sources_limit": 25,
            "schema": None,
        }
        default_args = {k: v for k, v in default_args.items() if k not in arguments}

        ai_crawler.crawl_async.assert_called_once_with(**default_args, **arguments)


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.AI_STUDIO_URL_ONLY,
        params.AI_STUDIO_URL_AND_OUTPUT_FORMAT,
        params.AI_STUDIO_URL_AND_SCHEMA,
        params.AI_STUDIO_URL_AND_RENDER_JAVASCRIPT,
        params.AI_STUDIO_URL_AND_GEO_LOCATION,
    ],
)
@pytest.mark.asyncio
async def test_ai_scraper(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    ai_scraper: AsyncMock,
):
    mock_result = MagicMock()
    mock_result.data = expected_result
    ai_scraper.scrape_async = AsyncMock(return_value=mock_result)

    arguments = {**arguments}

    with expectation:
        result = await mcp._call_tool("ai_scraper", arguments=arguments)

        assert result.content == [
            TextContent(type="text", text=json.dumps({"data": expected_result}))
        ]

        default_args = {
            "geo_location": None,
            "output_format": "markdown",
            "render_javascript": False,
            "schema": None,
        }
        default_args = {k: v for k, v in default_args.items() if k not in arguments}

        ai_scraper.scrape_async.assert_called_once_with(**default_args, **arguments)


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.AI_STUDIO_URL_ONLY,
        params.AI_STUDIO_URL_AND_OUTPUT_FORMAT,
        params.AI_STUDIO_URL_AND_SCHEMA,
        params.AI_STUDIO_URL_AND_GEO_LOCATION,
    ],
)
@pytest.mark.asyncio
async def test_ai_browser_agent(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    browser_agent: AsyncMock,
):
    mock_result = MagicMock()
    mock_data = SimpleSchema(title="Title", price=0.0)
    mock_result.data = mock_data
    browser_agent.run_async = AsyncMock(return_value=mock_result)

    arguments = {"task_prompt": "Scrape price and title", **arguments}

    with expectation:
        result = await mcp._call_tool("ai_browser_agent", arguments=arguments)

        assert result.content == [
            TextContent(type="text", text=json.dumps({"data": mock_data.model_dump()}))
        ]

        default_args = {
            "geo_location": None,
            "output_format": "markdown",
            "schema": None,
            "user_prompt": arguments["task_prompt"],
        }
        del arguments["task_prompt"]
        default_args = {k: v for k, v in default_args.items() if k not in arguments}

        browser_agent.run_async.assert_called_once_with(**default_args, **arguments)


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.AI_STUDIO_QUERY_ONLY,
        params.AI_STUDIO_URL_AND_RENDER_JAVASCRIPT,
        params.AI_STUDIO_URL_AND_GEO_LOCATION,
        params.AI_STUDIO_URL_AND_LIMIT,
        params.AI_STUDIO_QUERY_AND_RETURN_CONTENT,
    ],
)
@pytest.mark.asyncio
async def test_ai_search(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    ai_search: AsyncMock,
):
    mock_result = AiSearchJob(
        run_id="123",
        data=[SearchResult(url="url", title="title", description="description", content=None)],
    )
    ai_search.search_async = AsyncMock(return_value=mock_result)

    arguments = {**arguments}
    if "url" in arguments:
        del arguments["url"]
        arguments["query"] = "Sample query"

    with expectation:
        result = await mcp._call_tool("ai_search", arguments=arguments)

        assert result.content == [
            TextContent(type="text", text=json.dumps({"data": [mock_result.data[0].model_dump()]}))
        ]

        default_args = {
            "limit": 10,
            "render_javascript": False,
            "return_content": False,
            "geo_location": None,
        }
        default_args = {k: v for k, v in default_args.items() if k not in arguments}

        ai_search.search_async.assert_called_once_with(**default_args, **arguments)


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.AI_STUDIO_USER_PROMPT,
    ],
)
@pytest.mark.parametrize(
    "app_name",
    ["ai_crawler", "ai_scraper", "browser_agent"],
)
@pytest.mark.asyncio
async def test_generate_schema(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    app_name: str,
    ai_crawler: AsyncMock,
    ai_scraper: AsyncMock,
    browser_agent: AsyncMock,
    mock_schema: dict,
):
    arguments = {"app_name": app_name, **arguments}

    with expectation:
        result = await mcp._call_tool("generate_schema", arguments=arguments)

        assert result.content == [TextContent(type="text", text=json.dumps({"data": mock_schema}))]

        locals()[app_name].generate_schema.assert_called_once_with(prompt=arguments["user_prompt"])


@pytest.mark.parametrize(
    ("arguments", "expectation", "response_data", "expected_result"),
    [
        params.AI_STUDIO_URL_ONLY,
        params.AI_STUDIO_URL_AND_RENDER_JAVASCRIPT,
        params.AI_STUDIO_URL_AND_RETURN_SOURCES_LIMIT,
        params.AI_STUDIO_URL_AND_GEO_LOCATION,
    ],
)
@pytest.mark.asyncio
async def test_ai_map(
    mcp: FastMCP,
    request_data: Request,
    response_data: str,
    arguments: dict,
    expectation,
    expected_result: str,
    oxylabs_client: AsyncMock,
    ai_map: AsyncMock,
):
    mock_result = MagicMock()
    mock_result.data = expected_result
    ai_map.map_async = AsyncMock(return_value=mock_result)

    arguments = {"user_prompt": "Scrape price and title", **arguments}

    with expectation:
        result = await mcp._call_tool("ai_map", arguments=arguments)

        assert result.content == [
            TextContent(type="text", text=json.dumps({"data": expected_result}))
        ]

        default_args = {
            "geo_location": None,
            "render_javascript": False,
            "return_sources_limit": 25,
        }
        default_args = {k: v for k, v in default_args.items() if k not in arguments}

        ai_map.map_async.assert_called_once_with(**default_args, **arguments)
