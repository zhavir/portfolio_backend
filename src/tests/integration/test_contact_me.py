import pytest
from app.models import ContactForm
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_contact_me(test_client: AsyncClient) -> None:
    expected = {"text": "Email sent"}
    contact_form = ContactForm(
        from_email="test@test.it",
        subject="a-subject",
        text="text",
    )
    actual = await test_client.post(url="/api/v1/contact-me/", json=contact_form.model_dump())

    assert actual.status_code == status.HTTP_201_CREATED
    assert actual.json() == expected
