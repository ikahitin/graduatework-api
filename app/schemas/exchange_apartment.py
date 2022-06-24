import datetime
from enum import Enum
from typing import Optional, List

from pydantic import validator, EmailStr
from pydantic.main import BaseModel

from app.boto3.client import client
from app.core.config import SPACE_BUCKET_NAME
from app.schemas.auth import User
from app.schemas.general import Coordinates


class RoomTypeEnum(str, Enum):
    room = "кімната"
    bathroom = "ванна кімната"


class ExchangeDurationEnum(str, Enum):
    up_to_one_week = "до 1 тижня"
    one_two_weeks = "від 1 до 2 тижнів"
    one_three_weeks = "від 1 до 3 тижнів"
    three_or_more_weeks = "від 3 тижнів"


class Person(BaseModel):
    quantity: int


class Room(BaseModel):
    quantity: int


class RoomDescription(BaseModel):
    room: Room
    bathroom: Room


class PeopleDescription(BaseModel):
    adults: Person
    children: Person


class ExchangeApartmentBase(BaseModel):
    name: str
    description: str
    location: str
    coordinates: Coordinates
    city: str
    amenities: List[str]
    nearby: List[str]
    rooms: RoomDescription
    details: List[str]
    exchange_duration: ExchangeDurationEnum
    desired_city: Optional[str]
    people_quantity: PeopleDescription


class ExchangeApartmentCreate(ExchangeApartmentBase):
    pass


class ExchangeApartment(ExchangeApartmentBase):
    id: int
    images: Optional[List[str]]
    user: User

    class Config:
        orm_mode = True

    @validator("images", pre=True, check_fields=False)
    def validate_images_url(cls, v, values):
        if v:
            img_list = []
            for img in v:
                url = client.generate_presigned_url(ClientMethod="get_object",
                                                    Params={"Bucket": SPACE_BUCKET_NAME, "Key": f"exchange_apartment/{values['id']}/{img}"},
                                                    ExpiresIn=3600)
                img_list.append(url)
            return img_list


class ExchangeApartmentReservationBase(BaseModel):
    class Config:
        orm_mode = True

    from_date: datetime.date
    to_date: datetime.date
    guest_name: str
    guest_phone: str
    user_email: EmailStr
    apartment_id: int


class ExchangeApartmentReservationCreate(ExchangeApartmentReservationBase):
    pass


class ExchangeApartmentReservation(ExchangeApartmentReservationBase):
    id: int
    status: str
    apartment: ExchangeApartment
    # user: User
    created_at: datetime.date
