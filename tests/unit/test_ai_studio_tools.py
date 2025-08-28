import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from oxylabs_mcp.tools.ai_studio import (
    ai_browser_agent,
    ai_crawler,
    ai_scraper,
    ai_search,
    generate_schema,
)


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
    mocker,
    url,
    user_prompt,
    output_format,
    schema,
    render_javascript,
    return_sources_limit,
    request_context,
):
    """Test that the ai_crawler function returns the correct json format."""
    mock_crawler = MagicMock()
    mocker.patch("oxylabs_mcp.tools.ai_studio.AiCrawler", return_value=mock_crawler)

    mock_result = MagicMock()
    mock_result.data = {"test": "data"}
    mock_crawler.crawl_async = AsyncMock(return_value=mock_result)

    result = await ai_crawler.fn(
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
        geo_location=None,
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
async def test_ai_scraper(mocker, url, output_format, schema, render_javascript, request_context):
    """Test that the ai_scraper function returns the correct json format."""
    mock_scraper = MagicMock()
    mocker.patch("oxylabs_mcp.tools.ai_studio.AiScraper", return_value=mock_scraper)

    mock_result = MagicMock()
    mock_result.data = {"test": "data"}
    mock_scraper.scrape_async = AsyncMock(return_value=mock_result)

    result = await ai_scraper.fn(
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
        geo_location=None,
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
    mocker, url, task_prompt, output_format, schema, result_data, expected_result, request_context
):
    """Test that the ai_browser_agent function returns the correct json format."""
    mock_agent = MagicMock()
    mocker.patch("oxylabs_mcp.tools.ai_studio.BrowserAgent", return_value=mock_agent)

    mock_result = MagicMock()
    if result_data is not None:
        mock_result.data = MagicMock()
        mock_result.data.model_dump.return_value = result_data
    else:
        mock_result.data = None
    mock_agent.run_async = AsyncMock(return_value=mock_result)

    result = await ai_browser_agent.fn(
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
        geo_location=None,
    )


@pytest.mark.parametrize(
    ("query", "limit", "render_javascript", "return_content"),
    [
        pytest.param("test query", 10, False, False, id="default-params"),
        pytest.param("test query", 5, True, True, id="all-params"),
    ],
)
@pytest.mark.asyncio
async def test_ai_search(mocker, query, limit, render_javascript, return_content, request_context):
    """Test that the ai_search function returns the correct json format."""
    mock_search = MagicMock()
    mocker.patch("oxylabs_mcp.tools.ai_studio.AiSearch", return_value=mock_search)

    mock_result = MagicMock()
    mock_result.model_dump.return_value = {"data": {"results": []}}
    mock_search.search_async = AsyncMock(return_value=mock_result)

    result = await ai_search.fn(
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
        geo_location=None,
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
async def test_generate_schema_valid_apps(
    mocker, user_prompt, app_name, expected_schema, request_context
):
    """Test that the generate_schema function returns the correct json format."""
    mock_instance = MagicMock()
    mock_instance.generate_schema.return_value = expected_schema

    if app_name == "ai_crawler":
        mocker.patch("oxylabs_mcp.tools.ai_studio.AiCrawler", return_value=mock_instance)
    elif app_name == "ai_scraper":
        mocker.patch("oxylabs_mcp.tools.ai_studio.AiScraper", return_value=mock_instance)
    elif app_name == "browser_agent":
        mocker.patch("oxylabs_mcp.tools.ai_studio.BrowserAgent", return_value=mock_instance)

    result = await generate_schema.fn(user_prompt=user_prompt, app_name=app_name)

    assert result == json.dumps({"data": expected_schema})
    mock_instance.generate_schema.assert_called_once_with(prompt=user_prompt)


@pytest.mark.parametrize(
    ("user_prompt", "app_name"),
    [pytest.param("test", "invalid_app", id="invalid-app-name")],
)
@pytest.mark.asyncio
async def test_generate_schema_invalid_app(mocker, user_prompt, app_name, request_context):
    """Test that generate_schema raises ValueError for invalid app names."""
    with pytest.raises(ValueError, match=f"Invalid app name: {app_name}"):
        await generate_schema.fn(user_prompt=user_prompt, app_name=app_name)
