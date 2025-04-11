from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def oxylabs_client():
    client_mock = AsyncMock()

    @asynccontextmanager
    async def wrapper(*args, **kwargs):
        yield client_mock

    with patch("oxylabs_mcp.utils.AsyncClient", new=wrapper):
        yield client_mock
