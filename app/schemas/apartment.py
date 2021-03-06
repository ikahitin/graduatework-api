import datetime
from enum import Enum
from typing import Optional, List

from pydantic import validator, EmailStr
from pydantic.main import BaseModel

from app.boto3.client import client
from app.core.config import SPACE_BUCKET_NAME
from app.schemas.auth import User
from app.schemas.general import Coordinates


class Review(BaseModel):
    class Config:
        orm_mode = True

    id: int
    body: str
    rating: float
    created_at: datetime.date
    user: User


class ApartmentTypeEnum(str, Enum):
    city = "apartment"
    area = "hotel"
    hostel = "hostel"
    guest_house = "guest_house"
    resort_hotel = "resort_hotel"


class AmenityTypeEnum(str, Enum):
    free_parking = "Безкоштовна парковка"
    room_service = "Обслуговування номерів"
    free_wifi = "Безкоштовний WI-FI"


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
    rating: float
    apartment_type: ApartmentTypeEnum
    amenities: List[str]
    distance_from_center: int
    beds: Optional[List[BedDescription]]


class ApartmentCreate(ApartmentBase):
    pass


class Apartment(ApartmentBase):
    id: int
    images: Optional[List[str]]
    reviews: Optional[List[Review]]

    class Config:
        orm_mode = True

    @validator("images", pre=True, check_fields=False)
    def validate_images_url(cls, v, values):
        if v:
            img_list = []
            for img in v:
                url = client.generate_presigned_url(ClientMethod="get_object",
                                                    Params={"Bucket": SPACE_BUCKET_NAME, "Key": f"apartment/{values['id']}/{img}"},
                                                    ExpiresIn=3600)
                img_list.append(url)
            return img_list


class ApartmentReservationBase(BaseModel):
    class Config:
        orm_mode = True

    from_date: datetime.date
    to_date: datetime.date
    guest_name: str
    guest_phone: str
    comment: Optional[str]
    arriving_hour: int
    user_email: EmailStr
    apartment_id: int


class ApartmentReservationCreate(ApartmentReservationBase):
    pass


class ApartmentReservation(ApartmentReservationBase):
    id: int
    apartment: Apartment
    # user: User
    created_at: datetime.date
