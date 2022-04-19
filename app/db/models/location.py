from sqlalchemy import Column, Integer, String, Float

from app.db.session import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    region = Column(String)
    image_url = Column(String)
    rating = Column(Float)
    type = Column(String)
