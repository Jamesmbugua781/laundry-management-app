from .repository import CatalogRepository
from .service import CatalogService

def get_catalog_repo() -> CatalogRepository:
    return CatalogRepository()

def get_catalog_service() -> CatalogService:
    return CatalogService(get_catalog_repo())
