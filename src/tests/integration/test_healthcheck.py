import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(test_client: AsyncClient) -> None:
    actual = await test_client.get(url="/api/v1/healthcheck/")

    assert actual.status_code == status.HTTP_204_NO_CONTENT
