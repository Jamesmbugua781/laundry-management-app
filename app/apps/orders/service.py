from sqlalchemy.orm import Session
from .repository import OrderRepository
from .schemas import OrderCreate, OrderUpdate
from .models import Order

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, db: Session, user_id: int, order_in: OrderCreate) -> Order:
        return self.repo.create(db, user_id, order_in.model_dump())

    def get_order(self, db: Session, order_id: int) -> Order:
        return self.repo.get_by_id(db, order_id)

    def mark_as_paid(self, db: Session, order_id: int) -> Order:
        return self.repo.update(db, order_id, {"is_paid": True})

    def get_user_orders(self, db: Session, user_id: int):
        return self.repo.get_all_by_user(db, user_id)
