from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import LedgerEntry, TransactionType
from typing import List, Optional

class LedgerRepository:
    def create(self, db: Session, entry_data: dict) -> LedgerEntry:
        """
        Creates a new ledger entry. Immutable by design: no update or delete methods provided.
        """
        entry = LedgerEntry(**entry_data)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    def get_by_idempotency_key(self, db: Session, key: str) -> Optional[LedgerEntry]:
        return db.query(LedgerEntry).filter(LedgerEntry.idempotency_key == key).first()

    def get_user_history(self, db: Session, user_id: int, limit: int = 100) -> List[LedgerEntry]:
        return db.query(LedgerEntry).filter(
            LedgerEntry.user_id == user_id
        ).order_by(LedgerEntry.created_at.desc()).limit(limit).all()

    def calculate_balance(self, db: Session, user_id: int) -> float:
        """
        Calculates balance from ledger entries ONLY.
        Balance = SUM(Credits) - SUM(Debits)
        """
        # Sum credits
        credits = db.query(func.sum(LedgerEntry.amount)).filter(
            LedgerEntry.user_id == user_id,
            LedgerEntry.type == TransactionType.CREDIT
        ).scalar() or 0.0

        # Sum debits
        debits = db.query(func.sum(LedgerEntry.amount)).filter(
            LedgerEntry.user_id == user_id,
            LedgerEntry.type == TransactionType.DEBIT
        ).scalar() or 0.0

        return float(credits - debits)

    def get_entry_by_transaction_id(self, db: Session, transaction_id: str) -> List[LedgerEntry]:
        return db.query(LedgerEntry).filter(LedgerEntry.transaction_id == transaction_id).all()
