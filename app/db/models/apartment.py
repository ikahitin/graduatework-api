from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, func, Time
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import relationship

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
    # reservations = relationship("ApartmentReservation")
    reviews = relationship("ApartmentReview")


class ApartmentReservation(Base):
    __tablename__ = "apartment_reservation"

    id = Column(Integer, primary_key=True, index=True)
    from_date = Column(Date)
    to_date = Column(Date)
    guest_name = Column(String)
    guest_phone = Column(String)
    comment = Column(String)
    arriving_hour = Column(Integer)
    user_email = Column(String)
    created_at = Column(DateTime(), default=func.current_timestamp(), nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    apartment = relationship("Apartment")
    # user = relationship("User")


class ApartmentReview(Base):
    __tablename__ = "apartment_review"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    rating = Column(Float)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime(), default=func.current_timestamp(), nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartment.id'))
    user = relationship("User")
