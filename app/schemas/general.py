from enum import Enum

from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class ReservationStatusEnum(str, Enum):
    active = "active"
    planned = "planned"


class ReservationTypeEnum(str, Enum):
    all = "all"
    apartment = "apartment"
    car = "car"
    taxi = "taxi"
    exchange_vacation = "exchange_vacation"


class EmailSubscription(BaseModel):
    email: EmailStr
