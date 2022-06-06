from fastapi import APIRouter

from app.api.endpoints import auth, location, apartment, car, general, taxi, exchange_apartment

api_router = APIRouter()

api_router.include_router(
    general.router,
    prefix="",
    tags=["general"],
)

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

api_router.include_router(
    car.router,
    prefix="/car",
    tags=["car"],
)

api_router.include_router(
    taxi.router,
    prefix="/taxi",
    tags=["taxi"],
)

api_router.include_router(
    exchange_apartment.router,
    prefix="/exchange_apartment",
    tags=["exchange_apartment"],
)
