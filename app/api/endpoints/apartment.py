from typing import List

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.api.utils import get_db, apartment_params
from app.db import crud
from app.schemas.apartment import Apartment, ApartmentReservationCreate, ApartmentReservation

router = APIRouter()


@router.get("", response_model=List[Apartment])
async def get_apartments(db: Session = Depends(get_db), apartment_details: dict = Depends(apartment_params)):
    return crud.get_apartments(db=db, **apartment_details)


@router.get("/{apartment_id}", response_model=Apartment)
async def get_apartment_by_id(apartment_id: int, db: Session = Depends(get_db)):
    apartment = crud.get_apartment_by_id(db, apartment_id)
    if not apartment:
        raise HTTPException(
            status_code=404,
            detail="Apartment with this id does not exist",
        )

    return apartment


@router.post("/{apartment_id}/images", response_model=Apartment)
async def upload_apartment_images(apartment_id: int, images: List[UploadFile], db: Session = Depends(get_db)):
    apartment = await crud.add_apartment_images(db, images, apartment_id)
    return apartment


@router.post("/{apartment_id}/reservation", response_model=ApartmentReservation)
async def create_apartment_reservation(apartment_id: int, reservation: ApartmentReservationCreate, db: Session = Depends(get_db)):
    reservation = crud.create_apartment_reservation(db, apartment_id, reservation)
    return reservation
