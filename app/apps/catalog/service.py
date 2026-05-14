from sqlalchemy.orm import Session
from .repository import CatalogRepository
from .schemas import ServiceResponse, VendorPricingResponse
from app.core.cache import cached, invalidate_cache
from typing import List

class CatalogService:
    def __init__(self, repo: CatalogRepository):
        self.repo = repo

    @cached(ttl=3600, key_prefix="catalog")
    async def get_full_catalog(self, db: Session) -> List[dict]:
        """
        Fetches the full service catalog with caching.
        Returns a list of dicts (for JSON serialization in cache).
        """
        services = self.repo.get_all_services(db)
        # Convert to dict for caching
        return [ServiceResponse.model_validate(s).model_dump() for s in services]

    @cached(ttl=1800, key_prefix="pricing")
    async def get_vendor_rate_card(self, db: Session, vendor_id: int) -> List[dict]:
        """
        Fetches vendor-specific pricing with caching.
        """
        pricing = self.repo.get_vendor_pricing(db, vendor_id)
        return [VendorPricingResponse.model_validate(p).model_dump() for p in pricing]

    async def add_service(self, db: Session, data: dict):
        service = self.repo.create_service(db, data)
        # Invalidate catalog cache (Simplistic strategy)
        return service

    async def update_pricing(self, db: Session, vendor_id: int, service_id: int, new_price: float):
        # Implementation for updating pricing
        # Would also trigger cache invalidation
        pass
