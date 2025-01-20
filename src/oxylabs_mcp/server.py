from typing import Annotated, Any, Literal
from httpx import AsyncClient, Timeout, HTTPStatusError, RequestError
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
    async with AsyncClient(
        auth=get_auth_from_env(),
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


def main():
    mcp.run()


if __name__ == "__main__":
    main()
