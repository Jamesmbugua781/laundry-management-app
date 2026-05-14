from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from .models import TransactionType

class LedgerEntryBase(BaseModel):
    transaction_id: str
    user_id: int
    amount: float = Field(gt=0)
    type: TransactionType
    description: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    idempotency_key: str

class LedgerEntryCreate(LedgerEntryBase):
    pass

class LedgerEntryResponse(LedgerEntryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    user_id: int
    balance: float
