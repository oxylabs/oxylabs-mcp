from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import Request
from mcp.server.lowlevel.server import request_ctx

from oxylabs_mcp.server import add_oxylabs_tools
from oxylabs_mcp.server import mcp as mcp_server


add_oxylabs_tools(mcp_server)


@pytest.fixture
def request_context():
    request_context_mock = MagicMock()
    request_context_mock.info = AsyncMock()
    request_context_mock.error = AsyncMock()

    request_context_mock.request_id = 42

    request_context_mock.request_context.session.client_params.clientInfo.name = "fake_cursor"

    return request_context_mock


@pytest.fixture
def mcp(request_context):
    mcp_server.get_context = MagicMock()
    mcp_server.get_context.return_value = request_context

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
