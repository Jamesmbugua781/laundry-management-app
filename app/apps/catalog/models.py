from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Boolean
from app.core.database import Base
from typing import List, Optional

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, index=True, nullable=False) # e.g., Dry Clean, Wash & Fold
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    rate_cards: Mapped[List["RateCard"]] = relationship(back_populates="service")
    vendor_pricing: Mapped[List["VendorPricing"]] = relationship(back_populates="service")

class RateCard(Base):
    __tablename__ = "rate_cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False) # e.g., kg, piece
    base_price: Mapped[float] = mapped_column(Float, nullable=False)
    
    service: Mapped["Service"] = relationship(back_populates="rate_cards")

class VendorPricing(Base):
    __tablename__ = "vendor_pricing"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    custom_price: Mapped[float] = mapped_column(Float, nullable=False)
    discount_percentage: Mapped[float] = mapped_column(Float, default=0.0)

    service: Mapped["Service"] = relationship(back_populates="vendor_pricing")
