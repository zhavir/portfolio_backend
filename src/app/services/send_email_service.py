from app.core.boto_client_proxy import BotoClientProxy
from app.core.settings import get_settings
from app.models import ContactForm


class SendEmailService:
    def __init__(self, email_form: ContactForm, boto_client_proxy: BotoClientProxy) -> None:
        self._email_form = email_form
        self._boto_client_proxy = boto_client_proxy

    async def send_email(self) -> None:
        settings = get_settings()
        await self._boto_client_proxy.send_sns_message(
            Message=await self._get_message(
                from_email=self._email_form.from_email, subject=self._email_form.subject, text=self._email_form.text
            ),
            Subject=f"Personal Portfolio: {self._email_form.subject}",
            TopicArn=settings.aws.email_topic_arn,
        )

    async def _get_message(self, from_email: str, subject: str, text: str) -> str:
        return f"""Hello Andrea,
            new message received:

            from: {from_email},
            subject: {subject},
            text: {text}
        """
