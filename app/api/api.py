from fastapi import APIRouter

from app.api.endpoints import auth, location, apartment

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    location.router,
    prefix="/location",
    tags=["location"],
)

api_router.include_router(
    apartment.router,
    prefix="/apartment",
    tags=["apartment"],
)
