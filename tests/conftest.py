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
