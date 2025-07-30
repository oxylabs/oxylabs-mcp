import asyncio
import json
from contextlib import nullcontext as does_not_raise
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import FastMCP

from oxylabs_mcp.ai_studio.tools import (
    add_ai_studio_tools,
    ai_browser_agent,
    ai_crawler,
    ai_scraper,
    ai_search,
    generate_schema,
    is_ai_studio_api_key_available,
)


@pytest.mark.parametrize(
    ("api_key", "is_valid", "expectation", "should_call_validator"),
    [
        pytest.param(None, None, does_not_raise(), False, id="no-api-key"),
        pytest.param("invalid_key", False, pytest.raises(ValueError), True, id="invalid-api-key"),
        pytest.param("valid_key", True, does_not_raise(), True, id="valid-api-key"),
    ],
)
def test_is_ai_studio_api_key_available(
    mocker, api_key, is_valid, expectation, should_call_validator
):
    mocker.patch("oxylabs_mcp.ai_studio.tools.OXYLABS_AI_STUDIO_API_KEY", api_key)
    mock_is_valid = mocker.patch(
        "oxylabs_mcp.ai_studio.tools.is_api_key_valid", return_value=is_valid
    )

    with expectation:
        result = is_ai_studio_api_key_available()
        if api_key == "valid_key":
            assert result is True
        elif api_key is None:
            assert result is False

    # Check if is_api_key_valid was called
    if should_call_validator:
        mock_is_valid.assert_called_once_with(api_key)
    else:
        mock_is_valid.assert_not_called()


@pytest.mark.parametrize(
    ("url", "user_prompt", "output_format", "schema", "render_javascript", "return_sources_limit"),
    [
        pytest.param(
            "https://example.com",
            "extract info",
            "markdown",
            None,
            False,
            25,
            id="default-params",
        ),
        pytest.param(
            "https://example.com",
            "extract info",
            "json",
            {"type": "object", "properties": {"title": {"type": "string"}}},
            True,
            10,
            id="all-params",
        ),
    ],
)
@pytest.mark.asyncio
async def test_ai_crawler(
    mocker, url, user_prompt, output_format, schema, render_javascript, return_sources_limit
):
    """Test that the ai_crawler function returns the correct json format."""
    mock_crawler = MagicMock()
    mocker.patch("oxylabs_mcp.ai_studio.tools.AiCrawler", return_value=mock_crawler)

    mock_result = MagicMock()
    mock_result.data = {"test": "data"}
    mock_crawler.crawl_async = AsyncMock(return_value=mock_result)

    result = await ai_crawler(
        url=url,
        user_prompt=user_prompt,
        output_format=output_format,
        schema=schema,
        render_javascript=render_javascript,
        return_sources_limit=return_sources_limit,
    )

    assert result == '{"data": {"test": "data"}}'
    mock_crawler.crawl_async.assert_called_once_with(
        url=url,
        user_prompt=user_prompt,
        output_format=output_format,
        schema=schema,
        render_javascript=render_javascript,
        return_sources_limit=return_sources_limit,
    )


@pytest.mark.parametrize(
    ("url", "output_format", "schema", "render_javascript"),
    [
        pytest.param("https://example.com", "markdown", None, False, id="default-params"),
        pytest.param(
            "https://example.com",
            "json",
            {"type": "object", "properties": {"title": {"type": "string"}}},
            True,
            id="all-params",
        ),
    ],
)
@pytest.mark.asyncio
async def test_ai_scraper(mocker, url, output_format, schema, render_javascript):
    """Test that the ai_scraper function returns the correct json format."""
    mock_scraper = MagicMock()
    mocker.patch("oxylabs_mcp.ai_studio.tools.AiScraper", return_value=mock_scraper)

    mock_result = MagicMock()
    mock_result.data = {"test": "data"}
    mock_scraper.scrape_async = AsyncMock(return_value=mock_result)

    result = await ai_scraper(
        url=url,
        output_format=output_format,
        schema=schema,
        render_javascript=render_javascript,
    )

    assert result == '{"data": {"test": "data"}}'
    mock_scraper.scrape_async.assert_called_once_with(
        url=url,
        output_format=output_format,
        schema=schema,
        render_javascript=render_javascript,
    )


@pytest.mark.parametrize(
    ("url", "task_prompt", "output_format", "schema", "result_data", "expected_result"),
    [
        pytest.param(
            "https://example.com",
            "click button",
            "markdown",
            None,
            {"test": "data"},
            '{"data": {"test": "data"}}',
            id="default-params",
        ),
        pytest.param(
            "https://example.com",
            "click button",
            "json",
            {"type": "object", "properties": {"title": {"type": "string"}}},
            {"test": "data"},
            '{"data": {"test": "data"}}',
            id="with-schema",
        ),
        pytest.param(
            "https://example.com",
            "click button",
            "markdown",
            None,
            None,
            '{"data": null}',
            id="no-data",
        ),
    ],
)
@pytest.mark.asyncio
async def test_ai_browser_agent(
    mocker, url, task_prompt, output_format, schema, result_data, expected_result
):
    """Test that the ai_browser_agent function returns the correct json format."""
    mock_agent = MagicMock()
    mocker.patch("oxylabs_mcp.ai_studio.tools.BrowserAgent", return_value=mock_agent)

    mock_result = MagicMock()
    if result_data is not None:
        mock_result.data = MagicMock()
        mock_result.data.model_dump.return_value = result_data
    else:
        mock_result.data = None
    mock_agent.run_async = AsyncMock(return_value=mock_result)

    result = await ai_browser_agent(
        url=url,
        task_prompt=task_prompt,
        output_format=output_format,
        schema=schema,
    )

    assert result == expected_result
    mock_agent.run_async.assert_called_once_with(
        url=url,
        user_prompt=task_prompt,
        output_format=output_format,
        schema=schema,
    )


@pytest.mark.parametrize(
    ("query", "limit", "render_javascript", "return_content"),
    [
        pytest.param("test query", 10, False, False, id="default-params"),
        pytest.param("test query", 5, True, True, id="all-params"),
    ],
)
@pytest.mark.asyncio
async def test_ai_search(mocker, query, limit, render_javascript, return_content):
    """Test that the ai_search function returns the correct json format."""
    mock_search = MagicMock()
    mocker.patch("oxylabs_mcp.ai_studio.tools.AiSearch", return_value=mock_search)

    mock_result = MagicMock()
    mock_result.model_dump.return_value = {"data": {"results": []}}
    mock_search.search_async = AsyncMock(return_value=mock_result)

    result = await ai_search(
        query=query,
        limit=limit,
        render_javascript=render_javascript,
        return_content=return_content,
    )

    assert result == '{"data": {"results": []}}'
    mock_search.search_async.assert_called_once_with(
        query=query,
        limit=limit,
        render_javascript=render_javascript,
        return_content=return_content,
    )


@pytest.mark.parametrize(
    ("user_prompt", "app_name", "expected_schema"),
    [
        pytest.param("extract titles", "ai_crawler", {"type": "object"}, id="ai-crawler"),
        pytest.param("extract titles", "ai_scraper", {"type": "object"}, id="ai-scraper"),
        pytest.param("click button", "browser_agent", {"type": "object"}, id="browser-agent"),
    ],
)
@pytest.mark.asyncio
async def test_generate_schema_valid_apps(mocker, user_prompt, app_name, expected_schema):
    """Test that the generate_schema function returns the correct json format."""
    mock_instance = MagicMock()
    mock_instance.generate_schema.return_value = expected_schema

    if app_name == "ai_crawler":
        mocker.patch("oxylabs_mcp.ai_studio.tools.AiCrawler", return_value=mock_instance)
    elif app_name == "ai_scraper":
        mocker.patch("oxylabs_mcp.ai_studio.tools.AiScraper", return_value=mock_instance)
    elif app_name == "browser_agent":
        mocker.patch("oxylabs_mcp.ai_studio.tools.BrowserAgent", return_value=mock_instance)

    result = await generate_schema(user_prompt, app_name)

    assert result == json.dumps({"data": expected_schema})
    mock_instance.generate_schema.assert_called_once_with(prompt=user_prompt)


@pytest.mark.parametrize(
    ("user_prompt", "app_name"),
    [pytest.param("test", "invalid_app", id="invalid-app-name")],
)
@pytest.mark.asyncio
async def test_generate_schema_invalid_app(mocker, user_prompt, app_name):
    """Test that generate_schema raises ValueError for invalid app names."""
    with pytest.raises(ValueError, match=f"Invalid app name: {app_name}"):
        await generate_schema(user_prompt, app_name)


def test_add_ai_studio_tools():
    """Test that the AI studio tools are added to the MCP server."""

    mcp = FastMCP()

    add_ai_studio_tools(mcp)

    registered_tools = {i.name for i in asyncio.run(mcp.list_tools())}

    expected_tools = {
        "generate_schema",
        "ai_search",
        "ai_scraper",
        "ai_crawler",
        "ai_browser_agent",
    }

    assert (
        registered_tools == expected_tools
    ), f"Expected tools {expected_tools}, but got {registered_tools}"
