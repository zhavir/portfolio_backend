from fastapi import APIRouter, status

from app.core.logger import get_logger
from app.models import ContactForm, Message

router = APIRouter()


@router.post(
    "/contact-me/",
    status_code=status.HTTP_201_CREATED,
)
async def contact_me(email_form: ContactForm) -> Message:
    logger = get_logger()

    logger.info("Received request for sending email")

    return Message(text="Test email sent")
