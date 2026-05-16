from pydantic import BaseModel
from datetime import datetime


class STKPushRequest(BaseModel):
    order_id: int
    phone_number: str
    amount: int


class PaymentResponse(BaseModel):
    id: int
    amount: int
    phone_number: str
    status: str

    class Config:
        from_attributes = True


class MPESACallback(BaseModel):
    Body: dict