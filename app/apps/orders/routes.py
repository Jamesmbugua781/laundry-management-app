from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import RoleChecker, get_current_user_token_data, TokenData
from app.apps.users.providers import get_user_service
from app.apps.users.service import UserService

from .schemas import OrderCreate, OrderResponse
from .providers import get_order_service
from .service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service),
    user_service: UserService = Depends(get_user_service),
    current_user: TokenData = Depends(get_current_user_token_data)
):
    user = user_service.get_user_by_email(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return order_service.create_order(db, user.id, order_in)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service),
    user_service: UserService = Depends(get_user_service),
    current_user: TokenData = Depends(get_current_user_token_data)
):
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    user = user_service.get_user_by_email(db, current_user.email)
    
    # Ownership Check: Only owner or staff/admin can view
    if order.user_id != user.id and current_user.role not in ["staff", "admin", "receptionist"]:
        raise HTTPException(status_code=403, detail="Not enough permissions to view this order")
    
    return order

@router.patch("/{order_id}/mark-as-paid", response_model=OrderResponse)
def mark_order_as_paid(
    order_id: int,
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service),
    current_staff = Depends(RoleChecker(["staff", "receptionist", "admin"]))
):
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order_service.mark_as_paid(db, order_id)

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    order_service: OrderService = Depends(get_order_service),
    user_service: UserService = Depends(get_user_service),
    current_user: TokenData = Depends(get_current_user_token_data)
):
    user = user_service.get_user_by_email(db, current_user.email)
    
    if current_user.role in ["staff", "receptionist", "admin"]:
        return order_service.repo.get_all(db)
    
    return order_service.get_user_orders(db, user.id)
