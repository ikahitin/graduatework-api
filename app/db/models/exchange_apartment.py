from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql as pg

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
    # reviews = relationship("ApartmentReview")
