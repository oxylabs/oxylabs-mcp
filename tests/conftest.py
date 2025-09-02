from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp.server.context import Context, set_context
from httpx import Request
from mcp.server.lowlevel.server import request_ctx

from oxylabs_mcp import mcp as mcp_server


@pytest.fixture
def request_context():
    request_context = MagicMock()
    request_context.session.client_params.clientInfo.name = "fake_cursor"
    request_context.request.headers = {
        "x-oxylabs-username": "oxylabs_username",
        "x-oxylabs-password": "oxylabs_password",
        "x-oxylabs-ai-studio-api-key": "oxylabs_ai_studio_api_key",
    }

    ctx = Context(MagicMock())
    ctx.info = AsyncMock()
    ctx.error = AsyncMock()

    request_ctx.set(request_context)

    with set_context(ctx):
        yield ctx


@pytest.fixture(scope="session", autouse=True)
def environment():
    env = {
        "OXYLABS_USERNAME": "oxylabs_username",
        "OXYLABS_PASSWORD": "oxylabs_password",
        "OXYLABS_AI_STUDIO_API_KEY": "oxylabs_ai_studio_api_key",
    }
    with patch("os.environ", new=env):
        yield


@pytest.fixture
def mcp(request_context: Context):
    return mcp_server


@pytest.fixture
def request_data():
    return Request("POST", "https://example.com/v1/queries")


@pytest.fixture
def oxylabs_client():
    client_mock = AsyncMock()

    @asynccontextmanager
    async def wrapper(*args, **kwargs):
        client_mock.context_manager_call_args = args
        client_mock.context_manager_call_kwargs = kwargs

        yield client_mock

    with patch("oxylabs_mcp.utils.AsyncClient", new=wrapper):
        yield client_mock


@pytest.fixture
def request_session(request_context):
    token = request_ctx.set(request_context)

    yield request_context.session

    request_ctx.reset(token)


@pytest.fixture(scope="session", autouse=True)
def is_api_key_valid_mock():
    with patch("oxylabs_mcp.utils.is_api_key_valid", return_value=True):
        yield


@pytest.fixture
def mock_schema():
    return {"field_1": "value1", "field_2": "value2"}


@pytest.fixture
def ai_crawler(mock_schema):
    mock_crawler = MagicMock()
    mock_crawler.generate_schema.return_value = mock_schema

    with patch("oxylabs_mcp.tools.ai_studio.AiCrawler", return_value=mock_crawler):
        yield mock_crawler


@pytest.fixture
def ai_scraper(mock_schema):
    mock_scraper = MagicMock()
    mock_scraper.generate_schema.return_value = mock_schema

    with patch("oxylabs_mcp.tools.ai_studio.AiScraper", return_value=mock_scraper):
        yield mock_scraper


@pytest.fixture
def browser_agent(mock_schema):
    mock_browser_agent = MagicMock()
    mock_browser_agent.generate_schema.return_value = mock_schema

    with patch("oxylabs_mcp.tools.ai_studio.BrowserAgent", return_value=mock_browser_agent):
        yield mock_browser_agent


@pytest.fixture
def ai_search():
    mock_ai_search = MagicMock()

    with patch("oxylabs_mcp.tools.ai_studio.AiSearch", return_value=mock_ai_search):
        yield mock_ai_search


@pytest.fixture
def ai_map():
    mock_ai_map = MagicMock()

    with patch("oxylabs_mcp.tools.ai_studio.AiMap", return_value=mock_ai_map):
        yield mock_ai_map
