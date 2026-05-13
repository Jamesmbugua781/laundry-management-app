from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from .repository import AuthRepository
from .schemas import Token

class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def authenticate(self, db: Session, email: str, password: str) -> Token:
        user = self.repo.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return Token(access_token=access_token, token_type="bearer")
