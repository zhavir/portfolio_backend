from typing import AsyncGenerator

import pytest
from app.core.application import get_application
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    app = get_application()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:  # type: ignore
        yield client
