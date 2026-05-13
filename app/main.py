from fastapi import FastAPI
from app.core.settings import settings
from app.apps.auth.routes import router as auth_router
from app.apps.users.routes import router as users_router
from app.apps.orders.routes import router as orders_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Campus Laundry Management System API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Laundry Management API is running", "status": "ok"}
