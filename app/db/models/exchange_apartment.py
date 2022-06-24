from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

from app.db.session import Base


class ExchangeApartment(Base):
    __tablename__ = "exchange_apartment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    location = Column(String)
    coordinates = Column(pg.JSONB)
    city = Column(String)
    images = Column(pg.JSONB)
    amenities = Column(pg.JSONB)
    nearby = Column(pg.JSONB)
    rooms = Column(pg.JSONB)
    details = Column(pg.JSONB)
    exchange_duration = Column(pg.JSONB)
    desired_city = Column(String)
    people_quantity = Column(pg.JSONB)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")
    # reviews = relationship("ExchangeApartmentReview")


class ExchangeApartmentReservation(Base):
    __tablename__ = "exchange_apartment_reservation"

    id = Column(Integer, primary_key=True, index=True)
    from_date = Column(Date)
    to_date = Column(Date)
    guest_name = Column(String)
    guest_phone = Column(String)
    user_email = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime(), default=func.current_timestamp(), nullable=False)
    apartment_id = Column(Integer, ForeignKey('exchange_apartment.id'))
    apartment = relationship("ExchangeApartment")
