from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils import get_db
from app.db import crud
from app.schemas.location import LocationCreate, Location

router = APIRouter()


@router.get("", response_model=List[Location])
def get_locations(db: Session = Depends(get_db), location_type: Optional[str] = None):
    return crud.get_locations(db=db, location_type=location_type)


@router.post("", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db=db, location=location)
