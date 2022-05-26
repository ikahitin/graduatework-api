from typing import List

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.api.utils import get_db
from app.db import crud
from app.schemas.car import Car, CarCreate, CarReservation, CarReservationCreate

router = APIRouter()


@router.get("", response_model=List[Car])
async def get_cars(car_classification: str, db: Session = Depends(get_db)):
    return crud.get_cars(db, car_classification)


@router.get("/{car_id}", response_model=Car)
async def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(
            status_code=404,
            detail="Car with this id does not exist",
        )

    return car


@router.post("", response_model=Car)
async def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)


@router.post("/{car_id}/image_upload")
async def upload_car_image(car_id: int, image: UploadFile, db: Session = Depends(get_db)):
    return await crud.add_car_image(db, image, car_id)


@router.post("/{car_id}/reservation", response_model=CarReservation)
async def create_car_reservation(car_id: int, reservation: CarReservationCreate, db: Session = Depends(get_db)):
    reservation = crud.create_car_reservation(db, car_id, reservation)
    return reservation
