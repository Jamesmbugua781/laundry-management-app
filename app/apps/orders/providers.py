from .service import OrderService
from .repository import OrderRepository

def get_order_service():
    return OrderService(OrderRepository())
