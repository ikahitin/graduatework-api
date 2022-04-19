from enum import Enum
from typing import Optional

from pydantic import HttpUrl
from pydantic.main import BaseModel


class LocationTypeEnum(str, Enum):
    city = "city"
    area = "area"


class LocationBase(BaseModel):
    name: str
    region: str
    image_url: Optional[HttpUrl]
    rating: float
    type: LocationTypeEnum


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True
