import base64
import binascii
import json
import logging
import os
import re
import typing
from contextlib import asynccontextmanager
from importlib.metadata import version
from platform import architecture, python_version
from typing import AsyncIterator

from fastmcp.server.dependencies import get_context
from httpx import (
    AsyncClient,
    BasicAuth,
    HTTPStatusError,
    RequestError,
    Timeout,
)
from lxml.html import defs, fromstring, tostring
from lxml.html.clean import Cleaner
from markdownify import markdownify
from mcp.server.fastmcp import Context
from mcp.shared.context import RequestContext
from oxylabs_ai_studio.utils import is_api_key_valid  # type: ignore[import-untyped]
from starlette import status

from oxylabs_mcp.config import settings
from oxylabs_mcp.exceptions import MCPServerError


logger = logging.getLogger(__name__)

USERNAME_ENV = "OXYLABS_USERNAME"
PASSWORD_ENV = "OXYLABS_PASSWORD"  # noqa: S105  # nosec
AI_STUDIO_API_KEY_ENV = "OXYLABS_AI_STUDIO_API_KEY"

AUTHORIZATION_HEADER = "authorization"

# Header pairs accepted for Web Scraper API credentials, in priority order.
# The X-Oxylabs-* pair is the documented one; the underscore pair is kept for
# compatibility with clients configured against older deployments.
CREDENTIAL_HEADER_PAIRS = (
    ("x-oxylabs-username", "x-oxylabs-password"),
    ("oxylabs_username", "oxylabs_password"),
)

# Headers accepted for the AI Studio API key, in priority order.
AI_STUDIO_API_KEY_HEADERS = (
    "x-oxylabs-ai-studio-api-key",
    "oxylabs_ai_studio_api_key",
)

SCRAPER_CREDENTIALS_MISSING_HTTP = (
    "Oxylabs Web Scraper API credentials are not provided. "
    "Pass an 'Authorization: Basic <base64(username:password)>' header, "
    "or 'X-Oxylabs-Username' and 'X-Oxylabs-Password' headers. "
    "Get credentials at https://dashboard.oxylabs.io/"
)
SCRAPER_CREDENTIALS_MISSING_STDIO = (
    "Oxylabs Web Scraper API credentials are not provided. "
    "Set the OXYLABS_USERNAME and OXYLABS_PASSWORD environment variables "
    "in the MCP server configuration. "
    "Get credentials at https://dashboard.oxylabs.io/"
)
AI_STUDIO_API_KEY_MISSING_HTTP = (
    "Oxylabs AI Studio API key is not provided. "
    "Pass an 'X-Oxylabs-AI-Studio-Api-Key' header. "
    "Get your API key at https://aistudio.oxylabs.io/settings/api-key"
)
AI_STUDIO_API_KEY_MISSING_STDIO = (
    "Oxylabs AI Studio API key is not provided. "
    "Set the OXYLABS_AI_STUDIO_API_KEY environment variable "
    "in the MCP server configuration. "
    "Get your API key at https://aistudio.oxylabs.io/settings/api-key"
)


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
    return stripped_html


def _get_request_context(ctx: Context) -> RequestContext | None:  # type: ignore[type-arg]
    try:
        return ctx.request_context
    except ValueError:
        return None


def _get_default_headers() -> dict[str, str]:
    headers = {}
    if request_ctx := get_context().request_context:
        if client_params := request_ctx.session.client_params:
            client = f"oxylabs-mcp-{client_params.clientInfo.name}"
        else:
            client = "oxylabs-mcp"
    else:
        client = "oxylabs-mcp"

    bits, _ = architecture()
    sdk_type = f"{client}/{version('oxylabs-mcp')} ({python_version()}; {bits})"

    headers["x-oxylabs-sdk"] = sdk_type

    return headers


class _OxylabsClientWrapper:
    def __init__(
        self,
        client: AsyncClient,
    ) -> None:
        self._client = client
        self._ctx = get_context()

    async def scrape(self, payload: dict[str, typing.Any]) -> dict[str, typing.Any]:
        await self._ctx.info(f"Create job with params: {json.dumps(payload)}")

        response = await self._client.post(settings.OXYLABS_SCRAPER_URL, json=payload)
        response_json: dict[str, typing.Any] = response.json()

        if response.status_code == status.HTTP_201_CREATED:
            await self._ctx.info(
                f"Job info: "
                f"job_id={response_json['job']['id']} "
                f"job_status={response_json['job']['status']}"
            )

        response.raise_for_status()

        return response_json


def _parse_basic_auth(header_value: str) -> tuple[str | None, str | None]:
    """Parse an 'Authorization: Basic <credentials>' header value."""
    scheme, _, encoded = header_value.strip().partition(" ")
    if scheme.lower() != "basic" or not encoded:
        return None, None

    try:
        decoded = base64.b64decode(encoded.strip(), validate=True).decode()
    except (binascii.Error, UnicodeDecodeError):
        return None, None

    username, separator, password = decoded.partition(":")
    if not separator:
        return None, None

    return username or None, password or None


def get_oxylabs_auth() -> tuple[str | None, str | None]:
    """Extract the Oxylabs Web Scraper API credentials.

    With the HTTP transport, credentials are read from the request headers:
    the standard 'Authorization: Basic' header first, then the documented
    'X-Oxylabs-Username'/'X-Oxylabs-Password' pair, then the legacy
    underscore pair. With the stdio transport, credentials are read from
    the environment.
    """
    if settings.MCP_TRANSPORT == "streamable-http":
        request_headers = dict(get_context().request_context.request.headers)  # type: ignore[union-attr]

        if authorization := request_headers.get(AUTHORIZATION_HEADER):
            username, password = _parse_basic_auth(authorization)
            if username and password:
                return username, password

        for username_header, password_header in CREDENTIAL_HEADER_PAIRS:
            username = request_headers.get(username_header)
            password = request_headers.get(password_header)
            if username and password:
                return username, password

        return None, None

    return os.environ.get(USERNAME_ENV), os.environ.get(PASSWORD_ENV)


def get_oxylabs_ai_studio_api_key() -> str | None:
    """Extract the Oxylabs AI Studio API key."""
    if settings.MCP_TRANSPORT == "streamable-http":
        request_headers: dict[str, str] = dict(
            get_context().request_context.request.headers  # type: ignore[union-attr]
        )
        for header in AI_STUDIO_API_KEY_HEADERS:
            if ai_studio_api_key := request_headers.get(header):
                return ai_studio_api_key
        return None

    return os.getenv(AI_STUDIO_API_KEY_ENV)


@asynccontextmanager
async def oxylabs_client() -> AsyncIterator[_OxylabsClientWrapper]:
    """Async context manager for Oxylabs client that is used in MCP tools."""
    headers = _get_default_headers()

    username, password = get_oxylabs_auth()

    if not username or not password:
        if settings.MCP_TRANSPORT == "streamable-http":
            raise ValueError(SCRAPER_CREDENTIALS_MISSING_HTTP)
        raise ValueError(SCRAPER_CREDENTIALS_MISSING_STDIO)

    auth = BasicAuth(username=username, password=password)

    async with AsyncClient(
        timeout=Timeout(settings.OXYLABS_REQUEST_TIMEOUT_S),
        verify=True,
        headers=headers,
        auth=auth,
    ) as client:
        try:
            yield _OxylabsClientWrapper(client)
        except HTTPStatusError as e:
            raise MCPServerError(
                f"HTTP error during POST request: {e.response.status_code} - {e.response.text}"
            ) from None
        except RequestError as e:
            raise MCPServerError(f"Request error during POST request: {e}") from None
        except Exception as e:
            raise MCPServerError(f"Error: {str(e) or repr(e)}") from None


def get_and_verify_oxylabs_ai_studio_api_key() -> str:
    """Extract and verify the Oxylabs AI Studio API key."""
    ai_studio_api_key = get_oxylabs_ai_studio_api_key()

    if ai_studio_api_key is None:
        if settings.MCP_TRANSPORT == "streamable-http":
            msg = AI_STUDIO_API_KEY_MISSING_HTTP
        else:
            msg = AI_STUDIO_API_KEY_MISSING_STDIO
        logger.warning(msg)
        raise ValueError(msg)
    if not is_api_key_valid(ai_studio_api_key):
        raise ValueError(
            "The provided Oxylabs AI Studio API key is not valid. "
            "Check your API key at https://aistudio.oxylabs.io/settings/api-key"
        )

    return ai_studio_api_key


def extract_links_with_text(html: str, base_url: str | None = None) -> list[str]:
    """Extract links with their display text from HTML.

    Args:
        html (str): The input HTML string.
        base_url (str | None): Base URL to use for converting relative URLs to absolute.
                             If None, relative URLs will remain as is.

    Returns:
        list[str]: List of links in format [Display Text] URL

    """
    html_tree = fromstring(html)
    links = []

    for link in html_tree.xpath("//a[@href]"):  # type: ignore[union-attr]
        href = link.get("href")  # type: ignore[union-attr]
        text = link.text_content().strip()  # type: ignore[union-attr]

        if href and text:
            # Skip empty or whitespace-only text
            if not text:
                continue

            # Skip anchor links
            if href.startswith("#"):
                continue

            # Skip javascript links
            if href.startswith("javascript:"):
                continue

            # Make relative URLs absolute if base_url is provided
            if base_url and href.startswith("/"):
                # Remove trailing slash from base_url if present
                base = base_url.rstrip("/")
                href = f"{base}{href}"

            links.append(f"[{text}] {href}")

    return links


def _render_content(
    content: str | dict[str, typing.Any],
    *,
    output_format: str | None,
    parse: bool,
) -> str:
    if parse and isinstance(content, dict):
        return json.dumps(content)
    if output_format == "html":
        return str(content)
    if output_format == "links":
        links = extract_links_with_text(str(content))
        return "\n".join(links)

    stripped_html = clean_html(str(content))
    return markdownify(stripped_html)


def get_content(
    response_json: dict[str, typing.Any],
    *,
    output_format: str | None,
    parse: bool = False,
) -> str:
    """Extract content from response and convert to a proper format.

    A paginated request (`pages` > 1) returns one entry in `results` per page;
    every page is included in the output. Single-page responses keep the same
    output shape as before.
    """
    results = response_json["results"]
    contents = [result["content"] for result in results]

    if len(contents) == 1:
        return _render_content(contents[0], output_format=output_format, parse=parse)

    if parse and all(isinstance(content, dict) for content in contents):
        return json.dumps(contents)

    rendered_pages = (
        _render_content(content, output_format=output_format, parse=parse) for content in contents
    )
    return "\n\n".join(
        f"<!-- Page {number} -->\n{page}" for number, page in enumerate(rendered_pages, start=1)
    )
