import pytest
from app.core.settings import Settings
from app.models import Curriculum
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_generate_curriculum(settings: Settings, test_client: AsyncClient) -> None:
    expected = Curriculum(download_link=settings.application.cv_download_link)

    actual = await test_client.post(url="/api/v1/curriculum/")

    assert actual.status_code == status.HTTP_200_OK
    assert actual.json() == expected.model_dump()
