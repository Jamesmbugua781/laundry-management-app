from .service import AuthService
from .repository import AuthRepository

def get_auth_service():
    return AuthService(AuthRepository())
