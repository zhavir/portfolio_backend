from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    text: str


class ContactForm(BaseModel):
    from_email: EmailStr
    subject: str
    text: str
