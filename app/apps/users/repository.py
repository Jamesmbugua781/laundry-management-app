from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

class UserRepository:
    def create(self, db: Session, user_data: dict) -> User:
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
