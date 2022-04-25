from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils import get_db, apartment_params
from app.db import crud
from app.schemas.apartment import Apartment

router = APIRouter()


@router.get("", response_model=List[Apartment])
async def get_apartments(db: Session = Depends(get_db), apartment_details: dict = Depends(apartment_params)):
    return crud.get_apartments(db=db, **apartment_details)
