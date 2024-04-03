from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from src.core.application import get_application


@pytest.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    app = get_application()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:  # type: ignore
        yield client
