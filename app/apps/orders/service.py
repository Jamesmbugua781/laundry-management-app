from sqlalchemy.orm import Session
from loguru import logger
from .repository import OrderRepository
from .schemas import OrderCreate, OrderUpdate
from .models import Order, OrderStatus
from app.shared.exceptions import InvalidStatusTransition, PaymentRequired

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, db: Session, user_id: int, order_in: OrderCreate) -> Order:
        return self.repo.create(db, user_id, order_in.model_dump())

    def get_order(self, db: Session, order_id: int) -> Order:
        return self.repo.get_by_id(db, order_id)

    def mark_as_paid(self, db: Session, order_id: int) -> Order:
        return self.repo.update(db, order_id, {"is_paid": True})

    def update_order_status(
        self, db: Session, order_id: int, new_status: OrderStatus, actor_email: str = "system"
    ) -> Order:
        order = self.repo.get_by_id(db, order_id)
        if not order:
            return None

        current_status = order.status

        # Allow same status (idempotency)
        if current_status == new_status:
            return order
        
        # Define valid transitions
        valid_transitions = {
            OrderStatus.QUEUED: [OrderStatus.IN_PROGRESS, OrderStatus.READY],
            OrderStatus.IN_PROGRESS: [OrderStatus.READY],
            OrderStatus.READY: [OrderStatus.PICKED_UP]
        }

        allowed_next_statuses = valid_transitions.get(current_status, [])
        
        if new_status not in allowed_next_statuses:
            raise InvalidStatusTransition(
                f"Invalid transition from {current_status} to {new_status}. "
                f"Allowed transitions: {', '.join(allowed_next_statuses)}"
            )

        # Constraint Enforcement: Payment in Full
        if new_status == OrderStatus.PICKED_UP and not order.is_paid:
            raise PaymentRequired("Order must be paid in full before it can be PICKED_UP")

        updated_order = self.repo.update(db, order_id, {"status": new_status})

        # Structured Audit Trail Logging
        logger.bind(
            order_id=order_id,
            old_status=current_status,
            new_status=new_status,
            actor=actor_email
        ).info(f"Order status changed: {order_id} from {current_status} to {new_status} by {actor_email}")

        return updated_order

    def get_user_orders(self, db: Session, user_id: int):
        return self.repo.get_all_by_user(db, user_id)
