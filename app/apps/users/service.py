from sqlalchemy.orm import Session
from app.core.security import hash_password
from .repository import UserRepository
from .schemas import UserCreate
from .models import User
from app.shared.exceptions import UserAlreadyExists

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        existing_user = self.repo.get_by_email(db, user_in.email)
        if existing_user:
            raise UserAlreadyExists(f"User with email {user_in.email} already exists")
        
        user_data = user_in.model_dump()
        user_data["hashed_password"] = hash_password(user_data.pop("password"))
        
        return self.repo.create(db, user_data)

    def get_user_by_email(self, db: Session, email: str) -> User:
        return self.repo.get_by_email(db, email)
