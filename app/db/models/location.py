from sqlalchemy import Column, Integer, String, Float

from app.db.session import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    region = Column(String)
    image_url = Column(String)
    rating = Column(Float)
    location_type = Column(String)


class EmailSubscription(Base):
    __tablename__ = "email_subscription"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
