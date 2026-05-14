from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
import enum
from app.core.database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.apps.orders.models import Order

class UserRole(str, enum.Enum):
    STUDENT = "student"
    STAFF = "staff"
    RECEPTIONIST = "receptionist"
    ADMIN = "admin"
    VENDOR = "vendor"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default=UserRole.STUDENT, nullable=False)

    orders: Mapped[List["Order"]] = relationship(back_populates="owner")
