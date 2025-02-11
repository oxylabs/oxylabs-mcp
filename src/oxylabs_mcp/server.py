from typing import Annotated, Any, Literal
from httpx import AsyncClient, BasicAuth, Timeout, HTTPStatusError, RequestError
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import Field

from oxylabs_mcp.utils import convert_html_to_md, get_auth_from_env, strip_html

OXYLABS_SCRAPER_URL = "https://realtime.oxylabs.io/v1/queries"
REQUEST_TIMEOUT = 100

mcp = FastMCP("oxylabs_mcp", dependencies=["mcp", "httpx"])
load_dotenv()


@mcp.tool(name="oxylabs_scraper", description="Scrape url using Oxylabs Web Api")
async def scrape_url(
    url: Annotated[str, Field(description="Url to scrape")],
    parse: Annotated[
        bool | None,
        Field(
            description="Should result be parsed. "
            "If result should not be parsed then html "
            "will be stripped and converted to markdown file"
        )
    ] = None,
    render: Annotated[
        Literal["html", "None"] | None,
        Field(
            description="Whether a headless browser should be used "
            "to render the page. See: "
            "https://developers.oxylabs.io/scraper-apis/web-scraper-api/features/javascript-rendering "
            "`html` will return rendered html page "
            "`None` will not use render for scraping."
        )
    ] = None
) -> str:
    """Scrape Url using Oxylabs scraper api"""
    username, password = get_auth_from_env()

    async with AsyncClient(
        auth=BasicAuth(username=username, password=password),
        timeout=Timeout(REQUEST_TIMEOUT)
    ) as client:
        try:
            json: dict[str, Any] = {"url": url}
            if parse:
                json["parse"] = bool(parse)
            if render and render != "None":
                json["render"] = render

            response = await client.post(
                OXYLABS_SCRAPER_URL,
                json=json,
            )
            response.raise_for_status()

            if not bool(parse):
                striped_html = strip_html(
                    str(response.json()["results"][0]["content"])
                )
                return convert_html_to_md(striped_html)
            return str(response.json()["results"][0]["content"])
        except HTTPStatusError as e:
            return (
                "HTTP error during POST request: "
                f"{e.response.status_code} - {e.response.text}"
            )
        except RequestError as e:
            return f"Request error during POST request: {e}"
        except Exception as e:
            return f"Error: {str(e) or repr(e)}"


@mcp.tool(
    name="oxylabs_web_unblocker",
    description="Scrape url using Oxylabs Web Unblocker",
)
async def scrape_with_web_unblocker(
    url: Annotated[str, Field(description="Url to scrape with web unblocker")],
    render: Annotated[
        Literal["html", "None"] | None,
        Field(
            description="Whether a headless browser should be used "
            "to render the page. See: "
            "https://developers.oxylabs.io/advanced-proxy-solutions/web-unblocker/headless-browser/javascript-rendering "
            "`html` will return rendered html page "
            "`None` will not use render for scraping."
        )
    ] = None
) -> str:
    """Web Unblocker is an AI-powered proxy solution.

    This tool manages the unblocking process to extract public data
    even from the most difficult websites.
    """
    username, password = get_auth_from_env()

    proxy = f"http://{username}:{password}@unblock.oxylabs.io:60000"

    headers: dict[str, Any] = {}
    if render and render != "None":
        headers["X-Oxylabs-Render"] = render

    async with AsyncClient(
        timeout=Timeout(REQUEST_TIMEOUT),
        verify=False,
        proxy=proxy,
        headers=headers
    ) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            striped_html = strip_html(response.text)
            return convert_html_to_md(striped_html)
        except HTTPStatusError as e:
            return (
                "HTTP error during POST request: "
                f"{e.response.status_code} - {e.response.text}"
            )
        except RequestError as e:
            return f"Request error during POST request: {e}"
        except Exception as e:
            return f"Error: {str(e) or repr(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
