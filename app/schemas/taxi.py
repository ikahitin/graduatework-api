import datetime
from enum import Enum
from typing import Optional, Any

from pydantic import validator, EmailStr
from pydantic.main import BaseModel

from app.boto3.client import client
from app.core.config import SPACE_BUCKET_NAME


class TaxiType(str, Enum):
    standard = "Стандарт"
    upper_middle_class = "Вищий середній клас"
    minibus = "Мікроавтобус"


class UserAppealEnum(str, Enum):
    mister = "пан"
    miss = "пані"


class Location(BaseModel):
    start_latitude: float
    start_longitude: float
    end_latitude: float
    end_longitude: float


class TaxiBase(BaseModel):
    type: TaxiType
    capacity: int
    luggage_capacity: int
    price_for_km: int
    description: str


class TaxiCreate(TaxiBase):
    pass


class Taxi(TaxiBase):
    id: int
    image_url: Optional[str]
    price_for_ride: Any

    class Config:
        orm_mode = True
        use_enum_values = True

    @validator("image_url", pre=True, check_fields=False)
    def validate_image_url(cls, v):
        if v:
            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={'Bucket': SPACE_BUCKET_NAME, 'Key': f'taxi_images/{v}'},
                                                ExpiresIn=3600)
            return url


class TaxiReservationBase(BaseModel):
    class Config:
        orm_mode = True

    from_date: datetime.datetime
    to_date: datetime.datetime
    user_name: str
    user_phone: str
    user_email: EmailStr
    appeal: UserAppealEnum
    location: Location
    taxi_id: int


class TaxiReservationCreate(TaxiReservationBase):
    pass


class TaxiReservation(TaxiReservationBase):
    id: int
    taxi: Taxi
    ride_price: Optional[int]
    created_at: datetime.date
