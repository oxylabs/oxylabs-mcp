from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.server.lowlevel.server import request_ctx
from mcp.shared.context import RequestContext


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
def request_session():
    request_session_mock = MagicMock()

    token = request_ctx.set(
        RequestContext(
            42,
            None,
            request_session_mock,
            None,
        )
    )

    yield request_session_mock

    request_ctx.reset(token)
