import datetime
from enum import Enum
from typing import Optional, List

from pydantic import validator, HttpUrl, EmailStr
from pydantic.main import BaseModel

from app.boto3.client import client
from app.core.config import SPACE_BUCKET_NAME


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


class Addition(BaseModel):
    name: str
    quantity: int
    price: int


class CarAddition(BaseModel):
    additions: List[Addition]


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
    available: bool


class CarCreate(CarBase):
    image_url: Optional[str]


class Car(CarBase):
    id: int

    class Config:
        orm_mode = True
        use_enum_values = True

    @validator("image_url", pre=True, check_fields=False)
    def validate_image_url(cls, v):
        if v:
            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={'Bucket': SPACE_BUCKET_NAME, 'Key': f'car_images/{v}'},
                                                ExpiresIn=3600)
            return url


class CarReservationBase(BaseModel):
    class Config:
        orm_mode = True

    from_date: datetime.datetime
    to_date: datetime.datetime
    user_name: str
    user_phone: str
    user_email: EmailStr
    additions: Optional[CarAddition]
    car_id: int


class CarReservationCreate(CarReservationBase):
    pass


class CarReservation(CarReservationBase):
    id: int
    car: Car
    created_at: datetime.date
