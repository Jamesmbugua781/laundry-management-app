from sqlalchemy.orm import Session, joinedload
from .models import Order

class OrderRepository:
    def create(self, db: Session, user_id: int, data: dict) -> Order:
        order = Order(user_id=user_id, **data)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    def get_by_id(self, db: Session, order_id: int) -> Order:
        return db.query(Order).options(joinedload(Order.owner)).filter(Order.id == order_id).first()

    def get_all_by_user(self, db: Session, user_id: int):
        return db.query(Order).options(joinedload(Order.owner)).filter(Order.user_id == user_id).all()

    def get_all(self, db: Session):
        return db.query(Order).all()

    def update(self, db: Session, order_id: int, data: dict) -> Order:
        db.query(Order).filter(Order.id == order_id).update(data)
        db.commit()
        return self.get_by_id(db, order_id)
