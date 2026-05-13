from pydantic import BaseModel
from typing import Optional

class OrderBase(BaseModel):
    description: str
    amount: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    is_paid: Optional[bool] = None

class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: str
    is_paid: bool

    class Config:
        from_attributes = True
