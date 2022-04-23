from enum import Enum
from typing import Optional, List

from pydantic import HttpUrl
from pydantic.main import BaseModel

from app.schemas.general import Coordinates


class ApartmentTypeEnum(str, Enum):
    city = "apartment"
    area = "hotel"
    hostel = "hostel"
    guest_house = "guest_house"
    resort_hotel = "resort_hotel"


class BedDescription(BaseModel):
    bed_description: str
    quantity: int


class ApartmentBase(BaseModel):
    name: str
    description: str
    short_description: str
    location: str
    coordinates: Coordinates
    city: str
    price: int
    images: Optional[List[HttpUrl]]
    rating: float
    apartment_type: ApartmentTypeEnum
    amenities: List[str]
    distance_from_center: int
    beds: Optional[List[BedDescription]]


class ApartmentCreate(ApartmentBase):
    pass


class Apartment(ApartmentBase):
    id: int

    class Config:
        orm_mode = True
