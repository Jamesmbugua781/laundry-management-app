from pydantic import BaseModel


class SMSRequest(BaseModel):
    phone_number: str
    message: str


class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str