from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.api.utils import calc_distance
from app.db.session import Base


class Taxi(Base):
    __tablename__ = "taxi"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    image_url = Column(String)
    capacity = Column(Integer)
    luggage_capacity = Column(Integer)
    price_for_km = Column(Integer)
    description = Column(String)


class TaxiReservation(Base):
    __tablename__ = "taxi_reservation"

    id = Column(Integer, primary_key=True, index=True)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    appeal = Column(String)
    user_name = Column(String)
    user_phone = Column(String)
    user_email = Column(String)
    location = Column(pg.JSONB)
    created_at = Column(DateTime(), default=func.current_timestamp(), nullable=False)
    taxi_id = Column(Integer, ForeignKey('taxi.id'))
    taxi = relationship("Taxi")

    @hybrid_property
    def ride_price(self):
        dist = calc_distance(start_lat=self.location.get('start_latitude'),
                             start_lng=self.location.get('start_longitude'),
                             end_lat=self.location.get('end_latitude'),
                             end_lng=self.location.get('end_longitude'))
        price = int(dist * self.taxi.price_for_km)
        return price
