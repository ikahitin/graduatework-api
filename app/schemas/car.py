from enum import Enum
from typing import Optional

from pydantic import validator, HttpUrl
from pydantic.main import BaseModel

from app.core.config import BASE_URL


class CarCategoryEnum(str, Enum):
    small_car = "Малолітражні автомобілі"
    middle_class_car = "Автомобілі середнього класу"
    multi_seat_car = "Багатомісні автомобілі"
    premium_class_car = "Автомобілі преміум класу"
    suv = "Позашляховики"
    station_wagon = "Універсали"


class CarTransmissionEnum(str, Enum):
    automatic_transmission = "Автоматична коробка передач"
    manual_transmission = "Механічна коробка передач"


class CarInsurance(BaseModel):
    road_accident: bool
    theft: bool


class CarBase(BaseModel):
    name: str
    image_url: Optional[HttpUrl]
    capacity: int
    doors: int
    ac_included: bool
    insurance: CarInsurance
    location: str
    transmission: CarTransmissionEnum
    price: int
    provider: str
    category: CarCategoryEnum


class CarCreate(CarBase):
    image_url: Optional[str]


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

    @validator("image_url", pre=True, check_fields=False)
    def validate_image_url(cls, v):
        if v:
            return f"{BASE_URL}/static/car_images/{v}"