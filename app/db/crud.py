from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security.auth import get_password_hash
from app.db.models.location import Location
from app.db.models.user import User
from app.schemas.auth import UserCreate
from app.schemas.location import LocationCreate


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_location(db: Session, location: LocationCreate):
    obj_in_data = jsonable_encoder(location)
    db_location = Location(**obj_in_data)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def get_locations(db: Session, location_type: str = None):
    query = db.query(Location)
    if location_type:
        query = query.filter(Location.type == location_type)
    return query.all()


