from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.api.utils import get_db, save_image
from app.db import crud
from app.schemas.location import LocationCreate, Location, LocationTypeEnum

router = APIRouter()


@router.get("", response_model=List[Location])
async def get_locations(db: Session = Depends(get_db), order: str = "asc", location_type: Optional[str] = None):
    return crud.get_locations(db=db, order=order, location_type=location_type)


@router.post("", response_model=Location)
async def create_location(db: Session = Depends(get_db),
                          name: str = Form(...),
                          region: str = Form(...),
                          rating: float = Form(...),
                          location_type: LocationTypeEnum = Form(...),
                          image: UploadFile = File(None)):
    if image:
        image = await save_image(image, "location_images")

    location = LocationCreate(name=name, region=region, rating=rating, location_type=location_type, image_url=image)
    return crud.create_location(db=db, location=location)
