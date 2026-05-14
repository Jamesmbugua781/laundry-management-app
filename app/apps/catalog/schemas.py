from pydantic import BaseModel
from typing import List, Optional

class RateCardBase(BaseModel):
    unit: str
    base_price: float

class RateCardResponse(RateCardBase):
    id: int
    service_id: int

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    is_active: bool = True

class ServiceResponse(ServiceBase):
    id: int
    rate_cards: List[RateCardResponse] = []

    class Config:
        from_attributes = True

class VendorPricingBase(BaseModel):
    vendor_id: int
    service_id: int
    custom_price: float
    discount_percentage: float = 0.0

class VendorPricingResponse(VendorPricingBase):
    id: int

    class Config:
        from_attributes = True
