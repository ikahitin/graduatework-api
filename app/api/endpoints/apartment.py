from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.api.utils import get_db, apartment_params, save_image
from app.db import crud
from app.schemas.apartment import Apartment

router = APIRouter()


@router.get("", response_model=List[Apartment])
async def get_apartments(db: Session = Depends(get_db), apartment_details: dict = Depends(apartment_params)):
    return crud.get_apartments(db=db, **apartment_details)


@router.post("/{apartment_id}/images", response_model=Apartment)
async def upload_apartment_images(apartment_id: int, images: List[UploadFile], db: Session = Depends(get_db)):
    apartment = await crud.add_apartment_images(db, images, apartment_id)
    return apartment
