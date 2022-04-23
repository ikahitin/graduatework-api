from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects import postgresql as pg

from app.db.session import Base


class Apartment(Base):
    __tablename__ = "apartment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    short_description = Column(String)
    location = Column(String)
    coordinates = Column(pg.JSONB)
    city = Column(String)
    price = Column(Integer)
    images = Column(pg.JSONB)
    rating = Column(Float)
    apartment_type = Column(String)
    amenities = Column(pg.JSONB)
    distance_from_center = Column(Float)
    beds = Column(pg.JSONB)
