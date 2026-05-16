from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sys
from loguru import logger
from app.core.settings import settings
from app.apps.auth.routes import router as auth_router
from app.apps.users.routes import router as users_router
from app.apps.orders.routes import router as orders_router
from app.shared.exceptions import InvalidStatusTransition, PaymentRequired, UserAlreadyExists
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Structured Logging Configuration
logger.remove()
logger.add(
    sys.stdout, 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
    level="INFO",
    serialize=True # This enables JSON output for structured logs
)

app = FastAPI(
    title=settings.APP_NAME,
    description="Campus Laundry Management System API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(InvalidStatusTransition)
async def invalid_status_transition_handler(request: Request, exc: InvalidStatusTransition):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )

@app.exception_handler(PaymentRequired)
async def payment_required_handler(request: Request, exc: PaymentRequired):
    return JSONResponse(
        status_code=402,
        content={"detail": exc.message},
    )

@app.exception_handler(UserAlreadyExists)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Laundry Management API is running", "status": "ok"}
