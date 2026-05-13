from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import RoleChecker
from .schemas import UserCreate, UserResponse
from .providers import get_user_service
from .service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

# Only Admins can create new users through this endpoint (e.g., Staff/Receptionists)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    current_admin = Depends(RoleChecker(["admin"]))
):
    try:
        return service.create_user(db, user_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
def read_user_me(
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    current_user = Depends(RoleChecker(["student", "staff", "receptionist", "admin"]))
):
    user = service.get_user_by_email(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
