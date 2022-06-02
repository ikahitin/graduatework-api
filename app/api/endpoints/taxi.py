from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.api.utils import get_db, location_params
from app.db import crud
from app.schemas.taxi import Taxi, TaxiCreate, TaxiReservationCreate, TaxiReservation

router = APIRouter()


@router.get("", response_model=List[Taxi])
async def get_taxi(db: Session = Depends(get_db), location_details: dict = Depends(location_params)):
    return crud.get_taxi(db, location_details)


@router.get("/{taxi_id}", response_model=Taxi)
async def get_taxi_by_type(taxi_id: int, db: Session = Depends(get_db),
                           location_details: dict = Depends(location_params)):
    return crud.get_taxi_by_type(db, taxi_id, location_details)


@router.post("", response_model=Taxi)
async def create_taxi(taxi: TaxiCreate, db: Session = Depends(get_db)):
    return crud.create_taxi(db, taxi)


@router.post("/{taxi_type_id}/image_upload")
async def upload_taxi_image(taxi_type_id: int, image: UploadFile, db: Session = Depends(get_db)):
    return await crud.add_taxi_image(db, image, taxi_type_id)


@router.post("/{taxi_type_id}/reservation", response_model=TaxiReservation)
async def create_apartment_reservation(taxi_type_id: int, reservation: TaxiReservationCreate, db: Session = Depends(get_db)):
    reservation = crud.create_taxi_reservation(db, taxi_type_id, reservation)
    return reservation
