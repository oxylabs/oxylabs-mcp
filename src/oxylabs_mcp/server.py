from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from oxylabs_mcp import url_params
from oxylabs_mcp.config import settings
from oxylabs_mcp.exceptions import MCPServerError
from oxylabs_mcp.utils import (
    convert_html_to_md,
    get_content,
    oxylabs_client,
    strip_html,
)


mcp = FastMCP("oxylabs_mcp", dependencies=["mcp", "httpx"])


@mcp.tool(
    name="oxylabs_universal_scraper",
    description="Scrape url using Oxylabs Web API with universal scraper",
)
async def scrape_universal_url(
    ctx: Context,  # type: ignore[type-arg]
    url: url_params.URL_PARAM,
    parse: url_params.PARSE_PARAM = True,  # noqa: FBT002
    render: url_params.RENDER_PARAM = "",
) -> str:
    """Scrape url using Oxylabs Web API with universal scraper."""
    try:
        async with oxylabs_client(ctx, with_auth=True) as client:
            payload: dict[str, Any] = {"url": url}
            if parse:
                payload["parse"] = parse
            if render:
                payload["render"] = render

            response = await client.post(settings.OXYLABS_SCRAPER_URL, json=payload)

            response.raise_for_status()

            return get_content(response, parse)
    except MCPServerError as e:
        return e.stringify()


@mcp.tool(
    name="oxylabs_web_unblocker",
    description="Scrape url using Oxylabs Web Unblocker",
)
async def scrape_with_web_unblocker(
    ctx: Context,  # type: ignore[type-arg]
    url: url_params.URL_PARAM,
    render: url_params.RENDER_PARAM = "",
) -> str:
    """Scrape url using Oxylabs Web Unblocker.

    This tool manages the unblocking process to extract public data
    even from the most difficult websites.
    """
    headers: dict[str, Any] = {}
    if render:
        headers["X-Oxylabs-Render"] = render

    try:
        async with oxylabs_client(ctx, with_proxy=True, verify=False, headers=headers) as client:
            response = await client.get(url)

            response.raise_for_status()

            return convert_html_to_md(strip_html(response.text))
    except MCPServerError as e:
        return e.stringify()


@mcp.tool(
    name="oxylabs_google_search_scraper",
    description="Scrape Google Search results using Oxylabs Web API",
)
async def scrape_google_search(
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
) -> str:
    """Scrape Google Search results using Oxylabs Web API."""
    try:
        async with oxylabs_client(ctx, with_auth=True) as client:
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
            if geo_location:
                payload["locale"] = locale

            response = await client.post(settings.OXYLABS_SCRAPER_URL, json=payload)

            response.raise_for_status()

            return get_content(response, parse)
    except MCPServerError as e:
        return e.stringify()


@mcp.tool(
    name="oxylabs_amazon_search_scraper",
    description="Scrape Amazon Search results using Oxylabs Web API",
)
async def scrape_amazon_search(
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
) -> str:
    """Scrape Amazon Search results using Oxylabs Web API."""
    try:
        async with oxylabs_client(ctx, with_auth=True) as client:
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
            if geo_location:
                payload["locale"] = locale

            response = await client.post(settings.OXYLABS_SCRAPER_URL, json=payload)

            response.raise_for_status()

            return get_content(response, parse)
    except MCPServerError as e:
        return e.stringify()


@mcp.tool(
    name="oxylabs_amazon_product_scraper",
    description="Scrape Amazon Products using Oxylabs Web API",
)
async def scrape_amazon_products(
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
) -> str:
    """Scrape Amazon Products using Oxylabs Web API."""
    try:
        async with oxylabs_client(ctx, with_auth=True) as client:
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
            if geo_location:
                payload["locale"] = locale

            response = await client.post(settings.OXYLABS_SCRAPER_URL, json=payload)

            response.raise_for_status()

            return get_content(response, parse)
    except MCPServerError as e:
        return e.stringify()


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
