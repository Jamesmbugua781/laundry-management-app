from sqlalchemy.orm import Session
from .repository import LedgerRepository
from .schemas import LedgerEntryCreate, LedgerEntryResponse
from .models import TransactionType
from typing import List

class LedgerService:
    def __init__(self, repo: LedgerRepository):
        self.repo = repo

    def record_transaction(self, db: Session, entry_in: LedgerEntryCreate) -> LedgerEntryResponse:
        """
        Records a transaction with idempotency protection.
        """
        # Check if idempotency key already exists
        existing = self.repo.get_by_idempotency_key(db, entry_in.idempotency_key)
        if existing:
            return existing

        # Create new entry
        return self.repo.create(db, entry_in.model_dump())

    def get_user_balance(self, db: Session, user_id: int) -> float:
        return self.repo.calculate_balance(db, user_id)

    def get_transaction_history(self, db: Session, user_id: int) -> List[LedgerEntryResponse]:
        return self.repo.get_user_history(db, user_id)

    def record_payment(self, db: Session, user_id: int, amount: float, reference: str, idempotency_key: str):
        """
        Convenience method for recording a credit (payment).
        """
        entry_data = LedgerEntryCreate(
            transaction_id=reference,
            user_id=user_id,
            amount=amount,
            type=TransactionType.CREDIT,
            description=f"Payment reference: {reference}",
            idempotency_key=idempotency_key
        )
        return self.record_transaction(db, entry_data)

    def record_order_charge(self, db: Session, user_id: int, amount: float, order_id: str, idempotency_key: str):
        """
        Convenience method for recording a debit (order charge).
        """
        entry_data = LedgerEntryCreate(
            transaction_id=order_id,
            user_id=user_id,
            amount=amount,
            type=TransactionType.DEBIT,
            description=f"Order charge: {order_id}",
            idempotency_key=idempotency_key
        )
        return self.record_transaction(db, entry_data)
