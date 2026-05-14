import uuid
from typing import Optional

def generate_idempotency_key(prefix: str, identifier: str) -> str:
    """
    Generates a deterministic idempotency key.
    """
    return f"{prefix}:{identifier}"

def generate_transaction_id() -> str:
    """
    Generates a unique transaction ID.
    """
    return f"TXN-{uuid.uuid4().hex[:8].upper()}"
