from pydantic import BaseModel


class Message(BaseModel):
    text: str


class ContactForm(BaseModel):
    from_email: str
    subject: str
    text: str
