import os
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

from oxylabs_mcp import url_params
from oxylabs_mcp.ai_studio.tools import (
    add_ai_studio_tools,
    is_ai_studio_api_key_available,
)
from oxylabs_mcp.exceptions import MCPServerError
from oxylabs_mcp.utils import (
    get_content,
    is_oxylabs_credentials_available,
    oxylabs_client,
)


mcp = FastMCP(
    "oxylabs_mcp",
    log_level=os.getenv("LOG_LEVEL", "INFO"),
)


async def universal_scraper(
    ctx: Context,  # type: ignore[type-arg]
    url: url_params.URL_PARAM,
    render: url_params.RENDER_PARAM = "",
    user_agent_type: url_params.USER_AGENT_TYPE_PARAM = "",
    geo_location: url_params.GEO_LOCATION_PARAM = "",
    output_format: url_params.OUTPUT_FORMAT_PARAM = "",
) -> str:
    """Get a content of any webpage.

    Supports browser rendering, parsing of certain webpages
    and different output formats.
    """
    try:
        async with oxylabs_client(ctx) as client:
            payload: dict[str, Any] = {"url": url}

            if render:
                payload["render"] = render
            if user_agent_type:
                payload["user_agent_type"] = user_agent_type
            if geo_location:
                payload["geo_location"] = geo_location

            response_json = await client.scrape(payload)

            return get_content(response_json, output_format=output_format)
    except MCPServerError as e:
        return await e.process(ctx)


async def google_search_scraper(
    ctx: Context,  # type: ignore[type-arg]
    query: url_params.GOOGLE_QUERY_PARAM,
    parse: url_params.PARSE_PARAM = True,  # noqa: FBT002
    render: url_params.RENDER_PARAM = "",
    user_agent_type: url_params.USER_AGENT_TYPE_PARAM = "",
    start_page: url_params.START_PAGE_PARAM = 0,
    pages: url_params.PAGES_PARAM = 0,
    limit: url_params.LIMIT_PARAM = 0,
    domain: url_params.DOMAIN_PARAM = "",
    geo_location: url_params.GEO_LOCATION_PARAM = "",
    locale: url_params.LOCALE_PARAM = "",
    ad_mode: url_params.AD_MODE_PARAM = False,  # noqa: FBT002
    output_format: url_params.OUTPUT_FORMAT_PARAM = "",
) -> str:
    """Scrape Google Search results.

    Supports content parsing, different user agent types, pagination,
    domain, geolocation, locale parameters and different output formats.
    """
    try:
        async with oxylabs_client(ctx) as client:
            payload: dict[str, Any] = {"query": query}

            if ad_mode:
                payload["source"] = "google_ads"
            else:
                payload["source"] = "google_search"

            if parse:
                payload["parse"] = parse
            if render:
                payload["render"] = render
            if user_agent_type:
                payload["user_agent_type"] = user_agent_type
            if start_page:
                payload["start_page"] = start_page
            if pages:
                payload["pages"] = pages
            if limit:
                payload["limit"] = limit
            if domain:
                payload["domain"] = domain
            if geo_location:
                payload["geo_location"] = geo_location
            if locale:
                payload["locale"] = locale

            response_json = await client.scrape(payload)

            return get_content(response_json, parse=parse, output_format=output_format)
    except MCPServerError as e:
        return await e.process(ctx)


async def amazon_search_scraper(
    ctx: Context,  # type: ignore[type-arg]
    query: url_params.AMAZON_SEARCH_QUERY_PARAM,
    category_id: url_params.CATEGORY_ID_CONTEXT_PARAM = "",
    merchant_id: url_params.MERCHANT_ID_CONTEXT_PARAM = "",
    currency: url_params.CURRENCY_CONTEXT_PARAM = "",
    parse: url_params.PARSE_PARAM = True,  # noqa: FBT002
    render: url_params.RENDER_PARAM = "",
    user_agent_type: url_params.USER_AGENT_TYPE_PARAM = "",
    start_page: url_params.START_PAGE_PARAM = 0,
    pages: url_params.PAGES_PARAM = 0,
    domain: url_params.DOMAIN_PARAM = "",
    geo_location: url_params.GEO_LOCATION_PARAM = "",
    locale: url_params.LOCALE_PARAM = "",
    output_format: url_params.OUTPUT_FORMAT_PARAM = "",
) -> str:
    """Scrape Amazon search results.

    Supports content parsing, different user agent types, pagination,
    domain, geolocation, locale parameters and different output formats.
    Supports Amazon specific parameters such as category id, merchant id, currency.
    """
    try:
        async with oxylabs_client(ctx) as client:
            payload: dict[str, Any] = {"source": "amazon_search", "query": query}

            context = []
            if category_id:
                context.append({"key": "category_id", "value": category_id})
            if merchant_id:
                context.append({"key": "merchant_id", "value": merchant_id})
            if currency:
                context.append({"key": "currency", "value": currency})
            if context:
                payload["context"] = context

            if parse:
                payload["parse"] = parse
            if render:
                payload["render"] = render
            if user_agent_type:
                payload["user_agent_type"] = user_agent_type
            if start_page:
                payload["start_page"] = start_page
            if pages:
                payload["pages"] = pages
            if domain:
                payload["domain"] = domain
            if geo_location:
                payload["geo_location"] = geo_location
            if locale:
                payload["locale"] = locale

            response_json = await client.scrape(payload)

            return get_content(response_json, parse=parse, output_format=output_format)
    except MCPServerError as e:
        return await e.process(ctx)


async def amazon_product_scraper(
    ctx: Context,  # type: ignore[type-arg]
    query: url_params.AMAZON_SEARCH_QUERY_PARAM,
    autoselect_variant: url_params.AUTOSELECT_VARIANT_CONTEXT_PARAM = False,  # noqa: FBT002
    currency: url_params.CURRENCY_CONTEXT_PARAM = "",
    parse: url_params.PARSE_PARAM = True,  # noqa: FBT002
    render: url_params.RENDER_PARAM = "",
    user_agent_type: url_params.USER_AGENT_TYPE_PARAM = "",
    domain: url_params.DOMAIN_PARAM = "",
    geo_location: url_params.GEO_LOCATION_PARAM = "",
    locale: url_params.LOCALE_PARAM = "",
    output_format: url_params.OUTPUT_FORMAT_PARAM = "",
) -> str:
    """Scrape Amazon products.

    Supports content parsing, different user agent types, domain,
    geolocation, locale parameters and different output formats.
    Supports Amazon specific parameters such as currency and getting
    more accurate pricing data with auto select variant.
    """
    try:
        async with oxylabs_client(ctx) as client:
            payload: dict[str, Any] = {"source": "amazon_product", "query": query}

            context = []
            if autoselect_variant:
                context.append({"key": "autoselect_variant", "value": autoselect_variant})
            if currency:
                context.append({"key": "currency", "value": currency})
            if context:
                payload["context"] = context

            if parse:
                payload["parse"] = parse
            if render:
                payload["render"] = render
            if user_agent_type:
                payload["user_agent_type"] = user_agent_type
            if domain:
                payload["domain"] = domain
            if geo_location:
                payload["geo_location"] = geo_location
            if locale:
                payload["locale"] = locale

            response_json = await client.scrape(payload)

            return get_content(response_json, parse=parse, output_format=output_format)
    except MCPServerError as e:
        return await e.process(ctx)


def add_oxylabs_tools(mcp: FastMCP) -> None:
    """Add Oxylabs scraper API tools."""
    for tool in (
        universal_scraper,
        google_search_scraper,
        amazon_search_scraper,
        amazon_product_scraper,
    ):
        mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(tool)


def add_tools(mcp: FastMCP) -> None:
    """Add Oxylabs tools to the MCP server."""
    oxylabs_credentials_available = is_oxylabs_credentials_available()
    oxylabs_ai_studio_api_key_available = is_ai_studio_api_key_available()
    if not oxylabs_credentials_available and not oxylabs_ai_studio_api_key_available:
        message = (
            "Oxylabs credentials not set. "
            "To access universal, google and amazon scraper APIs "
            "please set 'OXYLABS_USERNAME' and 'OXYLABS_PASSWORD' environment variables."
            "To use Oxylabs AI Studio, set 'OXYLABS_AI_STUDIO_API_KEY' environment variable."
        )
        raise ValueError(message)

    if oxylabs_credentials_available:
        add_oxylabs_tools(mcp)

    if oxylabs_ai_studio_api_key_available:
        add_ai_studio_tools(mcp)


if __name__ == "__main__":
    add_tools(mcp)
    mcp.run()
