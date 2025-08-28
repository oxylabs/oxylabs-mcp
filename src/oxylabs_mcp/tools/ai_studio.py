# mypy: disable-error-code=import-untyped
import json
import logging
from typing import Annotated, Any, Literal

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from oxylabs_ai_studio.apps.ai_crawler import AiCrawler
from oxylabs_ai_studio.apps.ai_map import AiMap
from oxylabs_ai_studio.apps.ai_scraper import AiScraper
from oxylabs_ai_studio.apps.ai_search import AiSearch
from oxylabs_ai_studio.apps.browser_agent import (
    BrowserAgent,
)
from pydantic import Field

from oxylabs_mcp.utils import get_and_verify_oxylabs_ai_studio_api_key


logger = logging.getLogger(__name__)


AI_TOOLS = [
    "generate_schema",
    "ai_search",
    "ai_scraper",
    "ai_crawler",
    "ai_browser_agent",
    "ai_map",
]


mcp = FastMCP("ai_studio")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ai_crawler(
    url: Annotated[str, Field(description="The URL from which crawling will be started.")],
    user_prompt: Annotated[
        str,
        Field(description="What information user wants to extract from the domain."),
    ],
    output_format: Annotated[
        Literal["json", "markdown"],
        Field(
            description=(
                "The format of the output. If json, the schema is required. "
                "Markdown returns full text of the page."
            )
        ),
    ] = "markdown",
    schema: Annotated[
        dict[str, Any] | None,
        Field(
            description="The schema to use for the crawl. Only required if output_format is json."
        ),
    ] = None,
    render_javascript: Annotated[  # noqa: FBT002
        bool,
        Field(
            description=(
                "Whether to render the HTML of the page using javascript. Much slower, "
                "therefore use it only for websites "
                "that require javascript to render the page. "
                "Unless user asks to use it, first try to crawl the page without it. "
                "If results are unsatisfactory, try to use it."
            )
        ),
    ] = False,
    return_sources_limit: Annotated[
        int, Field(description="The maximum number of sources to return.", le=50)
    ] = 25,
    geo_location: Annotated[
        str | None, Field(description="Two letter ISO country code to use for the crawl proxy.")
    ] = None,
) -> str:
    """Tool useful for crawling a website from starting url and returning data in a specified format.

    Schema is required only if output_format is json.
    'render_javascript' is used to render javascript heavy websites.
    'return_sources_limit' is used to limit the number of sources to return,
    for example if you expect results from single source, you can set it to 1.
    """  # noqa: E501
    logger.info(
        f"Calling ai_crawler with: {url=}, {user_prompt=}, "
        f"{output_format=}, {schema=}, {render_javascript=}, "
        f"{return_sources_limit=}"
    )
    crawler = AiCrawler(api_key=get_and_verify_oxylabs_ai_studio_api_key())
    result = await crawler.crawl_async(
        url=url,
        user_prompt=user_prompt,
        output_format=output_format,
        schema=schema,
        render_javascript=render_javascript,
        return_sources_limit=return_sources_limit,
        geo_location=geo_location,
    )
    return json.dumps({"data": result.data})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ai_scraper(
    url: Annotated[str, Field(description="The URL to scrape")],
    output_format: Annotated[
        Literal["json", "markdown"],
        Field(
            description=(
                "The format of the output. If json, the schema is required. "
                "Markdown returns full text of the page."
            )
        ),
    ] = "markdown",
    schema: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "The schema to use for the scrape. Only required if output_format is json."
            )
        ),
    ] = None,
    render_javascript: Annotated[  # noqa: FBT002
        bool,
        Field(
            description=(
                "Whether to render the HTML of the page using javascript. "
                "Much slower, therefore use it only for websites "
                "that require javascript to render the page."
                "Unless user asks to use it, first try to scrape the page without it. "
                "If results are unsatisfactory, try to use it."
            )
        ),
    ] = False,
    geo_location: Annotated[
        str | None, Field(description="Two letter ISO country code to use for the scrape proxy.")
    ] = None,
) -> str:
    """Scrape the contents of the web page and return the data in the specified format.

    Schema is required only if output_format is json.
    'render_javascript' is used to render javascript heavy websites.
    """
    logger.info(
        f"Calling ai_scraper with: {url=}, {output_format=}, {schema=}, {render_javascript=}"
    )
    scraper = AiScraper(api_key=get_and_verify_oxylabs_ai_studio_api_key())
    result = await scraper.scrape_async(
        url=url,
        output_format=output_format,
        schema=schema,
        render_javascript=render_javascript,
        geo_location=geo_location,
    )
    return json.dumps({"data": result.data})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ai_browser_agent(
    url: Annotated[str, Field(description="The URL to start the browser agent navigation from.")],
    task_prompt: Annotated[str, Field(description="What browser agent should do.")],
    output_format: Annotated[
        Literal["json", "markdown", "html", "screenshot"],
        Field(
            description=(
                "The output format. Screenshot is base64 encoded jpeg image. "
                "Markdown returns full text of the page including links. "
                "If json, the schema is required."
            )
        ),
    ] = "markdown",
    schema: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "The schema to use for the scrape. Only required if output_format is json."
            )
        ),
    ] = None,
    geo_location: Annotated[
        str | None, Field(description="Two letter ISO country code to use for the browser proxy.")
    ] = None,
) -> str:
    """Run the browser agent and return the data in the specified format.

    This tool is useful if you need navigate around the website and do some actions.
    It allows navigating to any url, clicking on links, filling forms, scrolling, etc.
    Finally it returns the data in the specified format. Schema is required only if output_format is json.
    'task_prompt' describes what browser agent should achieve
    """  # noqa: E501
    logger.info(
        f"Calling ai_browser_agent with: {url=}, {task_prompt=}, {output_format=}, {schema=}"
    )
    browser_agent = BrowserAgent(api_key=get_and_verify_oxylabs_ai_studio_api_key())
    result = await browser_agent.run_async(
        url=url,
        user_prompt=task_prompt,
        output_format=output_format,
        schema=schema,
        geo_location=geo_location,
    )
    data = result.data.model_dump(mode="json") if result.data else None
    return json.dumps({"data": data})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ai_search(
    query: Annotated[str, Field(description="The query to search for.")],
    limit: Annotated[int, Field(description="Maximum number of results to return.", le=50)] = 10,
    render_javascript: Annotated[  # noqa: FBT002
        bool,
        Field(
            description=(
                "Whether to render the HTML of the page using javascript. "
                "Much slower, therefore use it only if user asks to use it."
                "First try to search with setting it to False. "
            )
        ),
    ] = False,
    return_content: Annotated[  # noqa: FBT002
        bool,
        Field(description="Whether to return markdown content of the search results."),
    ] = False,
    geo_location: Annotated[
        str | None, Field(description="Two letter ISO country code to use for the search proxy.")
    ] = None,
) -> str:
    """Search the web based on a provided query.

    'return_content' is used to return markdown content for each search result. If 'return_content'
        is set to True, you don't need to use ai_scraper to get the content of the search results urls,
        because it is already included in the search results.
    if 'return_content' is set to True, prefer lower 'limit' to reduce payload size.
    """  # noqa: E501
    logger.info(
        f"Calling ai_search with: {query=}, {limit=}, {render_javascript=}, {return_content=}"
    )
    search = AiSearch(api_key=get_and_verify_oxylabs_ai_studio_api_key())
    result = await search.search_async(
        query=query,
        limit=limit,
        render_javascript=render_javascript,
        return_content=return_content,
        geo_location=geo_location,
    )
    data = result.model_dump(mode="json")["data"]
    return json.dumps({"data": data})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def generate_schema(
    user_prompt: str,
    app_name: Literal["ai_crawler", "ai_scraper", "browser_agent"],
) -> str:
    """Generate a json schema in openapi format."""
    if app_name == "ai_crawler":
        crawler = AiCrawler(api_key=get_and_verify_oxylabs_ai_studio_api_key())
        schema = crawler.generate_schema(prompt=user_prompt)
    elif app_name == "ai_scraper":
        scraper = AiScraper(api_key=get_and_verify_oxylabs_ai_studio_api_key())
        schema = scraper.generate_schema(prompt=user_prompt)
    elif app_name == "browser_agent":
        browser_agent = BrowserAgent(api_key=get_and_verify_oxylabs_ai_studio_api_key())
        schema = browser_agent.generate_schema(prompt=user_prompt)
    else:
        raise ValueError(f"Invalid app name: {app_name}")

    return json.dumps({"data": schema})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ai_map(
    url: Annotated[str, Field(description="The URL from which URLs mapping will be started.")],
    user_prompt: Annotated[
        str,
        Field(description="What kind of urls user wants to find."),
    ],
    render_javascript: Annotated[  # noqa: FBT002
        bool,
        Field(
            description=(
                "Whether to render the HTML of the page using javascript. Much slower, "
                "therefore use it only for websites "
                "that require javascript to render the page. "
                "Unless user asks to use it, first try to crawl the page without it. "
                "If results are unsatisfactory, try to use it."
            )
        ),
    ] = False,
    return_sources_limit: Annotated[
        int, Field(description="The maximum number of sources to return.", le=50)
    ] = 25,
    geo_location: Annotated[
        str | None, Field(description="Two letter ISO country code to use for the mapping proxy.")
    ] = None,
) -> str:
    """Tool useful for mapping website's urls."""  # noqa: E501
    logger.info(
        f"Calling ai_map with: {url=}, {user_prompt=}, "
        f"{render_javascript=}, "
        f"{return_sources_limit=}"
    )
    ai_map = AiMap(api_key=get_and_verify_oxylabs_ai_studio_api_key())
    result = await ai_map.map_async(
        url=url,
        user_prompt=user_prompt,
        render_javascript=render_javascript,
        return_sources_limit=return_sources_limit,
        geo_location=geo_location,
    )
    return json.dumps({"data": result.data})
