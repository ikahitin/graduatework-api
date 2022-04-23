from pydantic.main import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float
