from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

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
    available = Column(String, default=True)


class CarReservation(Base):
    __tablename__ = "car_reservation"

    id = Column(Integer, primary_key=True, index=True)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    user_name = Column(String)
    user_phone = Column(String)
    user_email = Column(String)
    additions = Column(pg.JSONB)
    created_at = Column(DateTime(), default=func.current_timestamp(), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'))
    car = relationship("Car")
