from pydantic import BaseModel
from typing import Optional
from .models import OrderStatus

class OrderBase(BaseModel):
    description: str
    amount: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[OrderStatus] = None
    is_paid: Optional[bool] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    is_paid: bool

    class Config:
        from_attributes = True
