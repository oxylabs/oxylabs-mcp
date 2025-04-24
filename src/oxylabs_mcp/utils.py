import json
import os
import re
from contextlib import asynccontextmanager
from importlib.metadata import version
from platform import architecture, python_version
from typing import AsyncIterator

from httpx import (
    AsyncClient,
    BasicAuth,
    HTTPStatusError,
    RequestError,
    Response,
    Timeout,
)
from lxml.html import defs, fromstring, tostring
from lxml.html.clean import Cleaner
from markdownify import markdownify as md
from mcp.server.fastmcp import Context
from mcp.shared.context import RequestContext

from oxylabs_mcp.config import settings
from oxylabs_mcp.exceptions import MCPServerError


def get_auth_from_env() -> tuple[str, str]:
    """Get username and password from environment variables."""
    username = os.getenv("OXYLABS_USERNAME")
    password = os.getenv("OXYLABS_PASSWORD")

    if not username or not password:
        raise ValueError(
            "OXYLABS_USERNAME and OXYLABS_PASSWORD must be set in the environment variables."
        )
    return username, password


def clean_html(html: str) -> str:
    """Clean an HTML string."""
    cleaner = Cleaner(
        scripts=True,
        javascript=True,
        style=True,
        remove_tags=[],
        kill_tags=["nav", "svg", "footer", "noscript", "script", "form"],
        safe_attrs=list(defs.safe_attrs) + ["idx"],
        comments=True,
        inline_style=True,
        links=True,
        meta=False,
        page_structure=False,
        embedded=True,
        frames=False,
        forms=False,
        annoying_tags=False,
    )
    return cleaner.clean_html(html)  # type: ignore[no-any-return]


def strip_html(html: str) -> str:
    """Simplify an HTML string.

    Will remove unwanted elements, attributes, and redundant content
    Args:
        html (str): The input HTML string.

    Returns:
        str: The cleaned and simplified HTML string.

    """
    cleaned_html = clean_html(html)
    html_tree = fromstring(cleaned_html)

    for element in html_tree.iter():
        # Remove style attributes.
        if "style" in element.attrib:
            del element.attrib["style"]

        # Remove elements that have no attributes, no content and no children.
        if (
            (not element.attrib or (len(element.attrib) == 1 and "idx" in element.attrib))
            and not element.getchildren()  # type: ignore[attr-defined]
            and (not element.text or not element.text.strip())
            and (not element.tail or not element.tail.strip())
        ):
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)

    # Remove elements with footer and hidden in class or id
    xpath_query = (
        ".//*[contains(@class, 'footer') or contains(@id, 'footer') or "
        "contains(@class, 'hidden') or contains(@id, 'hidden')]"
    )
    elements_to_remove = html_tree.xpath(xpath_query)
    for element in elements_to_remove:  # type: ignore[assignment, union-attr]
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)

    # Serialize the HTML tree back to a string
    stripped_html = tostring(html_tree, encoding="unicode")
    # Previous cleaning produces empty spaces.
    # Replace multiple spaces with a single one
    stripped_html = re.sub(r"\s{2,}", " ", stripped_html)
    # Replace consecutive newlines with an empty string
    stripped_html = re.sub(r"\n{2,}", "", stripped_html)
    return stripped_html  # type: ignore[no-any-return]


def convert_html_to_md(html: str) -> str:
    """Convert HTML string to Markdown format."""
    return md(html)  # type: ignore[no-any-return]


def _get_request_context(ctx: Context) -> RequestContext | None:  # type: ignore[type-arg]
    try:
        return ctx.request_context
    except ValueError:
        return None


def _update_with_default_headers(
    ctx: Context, headers: dict[str, str]  # type: ignore[type-arg]
) -> None:
    if request_context := _get_request_context(ctx):
        if client_params := request_context.session.client_params:
            client = f"oxylabs-mcp-{client_params.clientInfo.name}"
        else:
            client = "oxylabs-mcp"
    else:
        client = "oxylabs-mcp"

    bits, _ = architecture()
    sdk_type = f"{client}/{version('oxylabs-mcp')} ({python_version()}; {bits})"

    headers["x-oxylabs-sdk"] = sdk_type


@asynccontextmanager
async def oxylabs_client(
    ctx: Context,  # type: ignore[type-arg]
    headers: dict[str, str] | None = None,
    *,
    with_proxy: bool = False,
    with_auth: bool = False,
    verify: bool = True,
) -> AsyncIterator[AsyncClient]:
    """Async context manager for Oxylabs client that is used in MCP tools."""
    if headers is None:
        headers = {}

    _update_with_default_headers(ctx, headers)

    username, password = get_auth_from_env()

    if with_proxy:
        proxy = f"http://{username}:{password}@unblock.oxylabs.io:60000"
    else:
        proxy = None

    if with_auth:
        auth = BasicAuth(username=username, password=password)
    else:
        auth = None

    async with AsyncClient(
        timeout=Timeout(settings.OXYLABS_REQUEST_TIMEOUT_S),
        verify=verify,
        proxy=proxy,
        headers=headers,
        auth=auth,
    ) as client:
        try:
            yield client
        except HTTPStatusError as e:
            raise MCPServerError(
                f"HTTP error during POST request: {e.response.status_code} - {e.response.text}"
            ) from None
        except RequestError as e:
            raise MCPServerError(f"Request error during POST request: {e}") from None
        except Exception as e:
            raise MCPServerError(f"Error: {str(e) or repr(e)}") from None


def get_content(response: Response, parse: bool | None = None) -> str:
    """Extract content from response and convert to a proper format."""
    content = response.json()["results"][0]["content"]

    if not bool(parse):
        striped_html = strip_html(str(content))
        return convert_html_to_md(striped_html)
    if isinstance(content, dict):
        return json.dumps(content)

    return str(content)
