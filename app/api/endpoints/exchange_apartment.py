from typing import List

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.api.utils import get_db, exchange_apartment_params
from app.core.security.auth import get_current_user
from app.db import crud
from app.schemas.auth import User
from app.schemas.exchange_apartment import ExchangeApartment, ExchangeApartmentCreate, ExchangeApartmentReservation, \
    ExchangeApartmentReservationCreate
from app.db.models.exchange_apartment import ExchangeApartment as DBExchangeApartment

router = APIRouter()


@router.get("", response_model=List[ExchangeApartment])
async def get_exchange_apartments(db: Session = Depends(get_db),
                                  exchange_apartment_details: dict = Depends(exchange_apartment_params)):
    return crud.get_exchange_apartments(db=db, **exchange_apartment_details)


@router.post("", response_model=ExchangeApartment)
async def create_exchange_apartment(apartment: ExchangeApartmentCreate, db: Session = Depends(get_db),
                                    current_user: User = Depends(get_current_user)):
    return crud.create_exchange_apartment(db, apartment, user_id=current_user.id)


@router.get("/{apartment_id}", response_model=ExchangeApartment)
async def get_exchange_apartment_by_id(apartment_id: int, db: Session = Depends(get_db)):
    apartment = crud.get_apartment_by_id(db, DBExchangeApartment, apartment_id)
    if not apartment:
        raise HTTPException(
            status_code=404,
            detail="Apartment with this id does not exist",
        )

    return apartment


@router.post("/{apartment_id}/images", response_model=ExchangeApartment)
async def upload_exchange_apartment_images(apartment_id: int, images: List[UploadFile], db: Session = Depends(get_db)):
    apartment = await crud.add_apartment_images(db, "exchange_apartment", images, DBExchangeApartment, apartment_id)
    return apartment


@router.post("/{apartment_id}/reservation", response_model=ExchangeApartmentReservation)
async def create_exchange_apartment_reservation(apartment_id: int, reservation: ExchangeApartmentReservationCreate, db: Session = Depends(get_db)):
    reservation = crud.create_exchange_apartment_reservation(db, reservation)
    return reservation
