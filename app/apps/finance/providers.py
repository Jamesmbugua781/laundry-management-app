from .repository import LedgerRepository
from .service import LedgerService

def get_ledger_repo() -> LedgerRepository:
    return LedgerRepository()

def get_ledger_service() -> LedgerService:
    return LedgerService(get_ledger_repo())
