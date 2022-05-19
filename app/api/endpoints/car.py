from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.api.utils import get_db
from app.db import crud
from app.schemas.car import Car, CarCreate

router = APIRouter()


@router.get("", response_model=List[Car])
async def get_cars(car_classification: str, db: Session = Depends(get_db)):
    return crud.get_cars(db, car_classification)


@router.post("", response_model=Car)
async def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)


@router.post("/{car_id}/image_upload")
async def upload_car_image(car_id: int, image: UploadFile, db: Session = Depends(get_db)):
    return await crud.add_car_image(db, image, car_id)
