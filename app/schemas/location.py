from enum import Enum
from typing import Optional

from pydantic import HttpUrl, validator
from pydantic.main import BaseModel

from app.boto3.client import client
from app.core.config import SPACE_BUCKET_NAME


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
            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={'Bucket': SPACE_BUCKET_NAME, 'Key': f'location_images/{v}'},
                                                ExpiresIn=3600)
            return url
