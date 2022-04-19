from enum import Enum
from typing import Optional

from pydantic import HttpUrl, validator
from pydantic.main import BaseModel

from app.core.config import BASE_URL


class LocationTypeEnum(str, Enum):
    city = "city"
    area = "area"


class LocationBase(BaseModel):
    name: str
    region: str
    image_url: Optional[HttpUrl]
    rating: float
    location_type: LocationTypeEnum


class LocationCreate(LocationBase):
    image_url: Optional[str]


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True

    @validator("image_url", pre=True, check_fields=False)
    def validate_image_url(cls, v):
        if v:
            return f"{BASE_URL}/static/location_images/{v}"
