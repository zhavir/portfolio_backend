from typing import AsyncGenerator, Generator
from unittest.mock import Mock

import pytest
from app.core.application import get_application
from app.core.boto_client_proxy import get_boto_client_proxy
from app.core.settings import Settings, get_settings
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture


@pytest.fixture
def settings() -> Settings:
    return get_settings()


@pytest.fixture
def mock_boto(mocker: MockerFixture) -> Generator[Mock, None, None]:
    yield mocker.patch(
        "app.core.application.get_boto_client_proxy",
        return_value=get_boto_client_proxy(region_name="us-east-1", session=Mock()),
    )


@pytest.fixture
async def test_client(mock_boto: Mock) -> AsyncGenerator[AsyncClient, None]:
    app = get_application()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:  # type: ignore
        yield client
