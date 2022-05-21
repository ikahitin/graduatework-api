from datetime import date
from typing import List

from fastapi import UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from app.api.utils import save_image
from app.core.security.auth import get_password_hash
from app.db.models.apartment import Apartment, ApartmentReservation
from app.db.models.car import Car
from app.db.models.location import Location
from app.db.models.user import User
from app.schemas.apartment import ApartmentReservationCreate
from app.schemas.auth import UserCreate
from app.schemas.car import CarCreate, CarCategoryEnum
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


def get_locations(db: Session, order: str, location_type: str = None):
    query = db.query(Location)
    if order == "desc":
        query = db.query(Location).order_by(Location.id.desc())
    if location_type:
        query = query.filter(Location.location_type == location_type)
    return query.order_by(Location.id).all()


def get_apartments(db: Session, **kwargs):
    booked_apartments = db.query(ApartmentReservation.apartment_id).filter(
        (ApartmentReservation.from_date.between(kwargs["start"], kwargs["end"]) |
         ApartmentReservation.to_date.between(kwargs["start"], kwargs["end"])))

    available_apartments = db.query(Apartment).filter(Apartment.id.not_in(booked_apartments))
    query = available_apartments.filter(Apartment.city == kwargs["city"])
    return query.all()


def get_apartment_by_id(db: Session, apartment_id: int):
    query = db.query(Apartment).filter(Apartment.id == apartment_id)
    return query.first()


async def add_apartment_images(db: Session, images: List[UploadFile], apartment_id: int):
    img_list = []
    for img in images:
        filename = await save_image(img, f"apartment/{apartment_id}")
        img_list.append(filename)
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    apartment.images = img_list
    db.add(apartment)
    db.commit()
    db.refresh(apartment)
    return apartment


def get_cars(db: Session, categoryf: str):
    query = db.query(Car).filter(Car.category == CarCategoryEnum[categoryf].value)
    return query.all()


def create_car(db: Session, car: CarCreate):
    obj_in_data = jsonable_encoder(car)
    db_car = Car(**obj_in_data)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


async def add_car_image(db: Session, image: UploadFile, car_id: int):
    filename = await save_image(image, f"car_images")
    car = db.query(Car).filter(Car.id == car_id).first()
    car.image_url = filename
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def check_if_apartment_available(db: Session, apartment_id, from_date, to_date):
    booked_apartments = db.query(ApartmentReservation.apartment_id).filter(
        (ApartmentReservation.from_date.between(from_date, to_date) |
         ApartmentReservation.to_date.between(from_date, to_date)))

    return db.query(Apartment).filter(Apartment.id.not_in(booked_apartments)).filter(Apartment.id == apartment_id).scalar() is not None


def create_apartment_reservation(db: Session, apartment_id: int, reservation: ApartmentReservationCreate):
    apartment_available = check_if_apartment_available(db, apartment_id, reservation.from_date, reservation.to_date)
    if not apartment_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apartment is not available in those dates")

    obj_in_data = jsonable_encoder(reservation)
    db_reservation = ApartmentReservation(**obj_in_data)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def get_reservations(db: Session, current_user_email, reservation_status: str, reservation_type: str):
    today = date.today()
    query = db.query(ApartmentReservation)
    if reservation_type == "apartment":
        query = query.filter(ApartmentReservation.user_email == current_user_email)
    if reservation_status == "planned":
        query = query.filter((ApartmentReservation.from_date > today))
    elif reservation_status == "active":
        query = query.filter(
            (ApartmentReservation.from_date.between(today, today) |
             ApartmentReservation.to_date.between(today, today)))
    return query.all()


