from fastapi import APIRouter, Request, status

from app.core.boto_client_proxy import BotoClientProxy
from app.core.logger import get_logger
from app.models import ContactForm, Message
from app.services.send_email_service import SendEmailService

router = APIRouter()


@router.post(
    "/contact-me/",
    status_code=status.HTTP_201_CREATED,
)
async def contact_me(request: Request, email_form: ContactForm) -> Message:
    logger = get_logger()
    await logger.ainfo("Received request for sending email")
    boto_client_proxy: BotoClientProxy = request.app.extra["boto_client_proxy"]
    await SendEmailService(email_form=email_form, boto_client_proxy=boto_client_proxy).send_email()
    await logger.ainfo("Email sent successfully")
    return Message(text="Email sent")
