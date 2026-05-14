from sqlalchemy.orm import Session, joinedload
from .models import Service, RateCard, VendorPricing
from typing import List, Optional

class CatalogRepository:
    def get_all_services(self, db: Session) -> List[Service]:
        """
        Uses joinedload to eliminate N+1 queries for rate cards.
        """
        return db.query(Service).options(
            joinedload(Service.rate_cards)
        ).filter(Service.is_active == True).all()

    def get_service_by_id(self, db: Session, service_id: int) -> Optional[Service]:
        return db.query(Service).options(
            joinedload(Service.rate_cards)
        ).filter(Service.id == service_id).first()

    def get_vendor_pricing(self, db: Session, vendor_id: int) -> List[VendorPricing]:
        return db.query(VendorPricing).options(
            joinedload(VendorPricing.service)
        ).filter(VendorPricing.vendor_id == vendor_id).all()

    def create_service(self, db: Session, data: dict) -> Service:
        service = Service(**data)
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    def create_rate_card(self, db: Session, data: dict) -> RateCard:
        rate_card = RateCard(**data)
        db.add(rate_card)
        db.commit()
        db.refresh(rate_card)
        return rate_card

    def create_vendor_pricing(self, db: Session, data: dict) -> VendorPricing:
        vp = VendorPricing(**data)
        db.add(vp)
        db.commit()
        db.refresh(vp)
        return vp
