from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects import postgresql as pg

from app.db.session import Base


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image_url = Column(String)
    capacity = Column(Integer)
    doors = Column(Integer)
    ac_included = Column(Boolean)
    insurance = Column(pg.JSONB)
    location = Column(String)
    transmission = Column(pg.JSONB)
    price = Column(Integer)
    provider = Column(String)
    category = Column(String)
