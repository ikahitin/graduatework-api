from datetime import date
from typing import List

from fastapi import UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Integer, and_
from sqlalchemy.orm import Session
from starlette import status

from app.api.utils import save_image, calc_price_in_taxi_query, add_price_obj
from app.core.security.auth import get_password_hash
from app.db.models.apartment import Apartment, ApartmentReservation
from app.db.models.car import Car, CarReservation
from app.db.models.exchange_apartment import ExchangeApartment, ExchangeApartmentReservation
from app.db.models.location import EmailSubscription as EmailSubscriptionDB
from app.db.models.location import Location
from app.db.models.taxi import Taxi, TaxiReservation
from app.db.models.user import User
from app.db.session import Base
from app.schemas.apartment import ApartmentReservationCreate, ApartmentCreate
from app.schemas.auth import UserCreate
from app.schemas.car import CarCreate, CarCategoryEnum, CarReservationCreate
from app.schemas.exchange_apartment import ExchangeApartmentCreate, ExchangeApartmentReservationCreate
from app.schemas.general import EmailSubscription
from app.schemas.location import LocationCreate
from app.schemas.taxi import TaxiCreate, TaxiReservationCreate


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


def get_apartment_by_id(db: Session, model: Base, apartment_id: int):
    query = db.query(model).filter(model.id == apartment_id)
    return query.first()


def get_car_by_id(db: Session, car_id: int):
    query = db.query(Car).filter(Car.id == car_id)
    return query.first()


async def add_apartment_images(db: Session, img_folder: str, images: List[UploadFile], model: Base, apartment_id: int):
    img_list = []
    for img in images:
        filename = await save_image(img, f"{img_folder}/{apartment_id}")
        img_list.append(filename)
    apartment = db.query(model).filter(model.id == apartment_id).first()
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

    return db.query(Apartment).filter(Apartment.id.not_in(booked_apartments)).filter(
        Apartment.id == apartment_id).scalar() is not None


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
    if reservation_type == "apartment":
        model = ApartmentReservation
    elif reservation_type == "car":
        model = CarReservation
    elif reservation_type == "taxi":
        model = TaxiReservation
    query = db.query(model)
    query = query.filter(model.user_email == current_user_email)
    if reservation_status == "planned":
        query = query.filter((model.from_date > today))
    elif reservation_status == "active":
        print(today)
        # query = query.filter(
        #     (model.from_date.between(today, today) |
        #      model.to_date.between(today, today)))
        query = query.filter(
        and_(today <= model.to_date, today >= model.from_date))
    return query.all()


def create_apartment(db: Session, apartment: ApartmentCreate):
    obj_in_data = jsonable_encoder(apartment)
    apartment = Apartment(**obj_in_data)
    db.add(apartment)
    db.commit()
    db.refresh(apartment)
    return apartment


def create_car_reservation(db: Session, car_id: int, reservation: CarReservationCreate):
    car = db.query(Car).get(car_id)
    if car:
        if not car.available:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Car is not available for booking")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car with id does not exist")

    obj_in_data = jsonable_encoder(reservation)
    db_reservation = CarReservation(**obj_in_data)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def get_taxi(db: Session, location_details):
    query = db.query(Taxi)
    results = calc_price_in_taxi_query(query, location_details)
    return results


def get_taxi_by_type(db: Session, taxi_id: int, location_details):
    query = db.query(Taxi).filter(Taxi.id == taxi_id)
    obj = add_price_obj(query.first(), location_details)
    return obj


def create_taxi(db: Session, taxi: TaxiCreate):
    obj_in_data = jsonable_encoder(taxi)
    db_taxi = Taxi(**obj_in_data)
    db.add(db_taxi)
    db.commit()
    db.refresh(db_taxi)
    return db_taxi


async def add_taxi_image(db: Session, image: UploadFile, taxi_id: int):
    filename = await save_image(image, "taxi_images")
    taxi = db.query(Taxi).filter(Taxi.id == taxi_id).first()
    taxi.image_url = filename
    db.add(taxi)
    db.commit()
    db.refresh(taxi)
    return taxi


def create_taxi_reservation(db: Session, taxi_type_id: int, reservation: TaxiReservationCreate):
    obj_in_data = jsonable_encoder(reservation)
    db_reservation = TaxiReservation(**obj_in_data)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def get_exchange_apartments(db: Session, **kwargs):
    query = db.query(ExchangeApartment) \
        .filter(ExchangeApartment.city == kwargs.get("city")) \
        .filter(
        (ExchangeApartment.desired_city == kwargs.get("proposed_city")) | (ExchangeApartment.desired_city == None)) \
        .filter(ExchangeApartment.people_quantity["adults"]["quantity"].cast(Integer) <= kwargs.get("adults")) \
        .filter(ExchangeApartment.people_quantity["children"]["quantity"].cast(Integer) <= kwargs.get("children"))
    return query.all()


def create_exchange_apartment(db: Session, apartment: ExchangeApartmentCreate, user_id: int):
    obj_in_data = jsonable_encoder(apartment)
    apartment = ExchangeApartment(**obj_in_data)
    apartment.user_id = user_id
    db.add(apartment)
    db.commit()
    db.refresh(apartment)
    return apartment


def create_exchange_apartment_reservation(db: Session, reservation: ExchangeApartmentReservationCreate):
    obj_in_data = jsonable_encoder(reservation)
    db_reservation = ExchangeApartmentReservation(**obj_in_data)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def add_email(db: Session, email_body: EmailSubscription):
    obj_in_data = jsonable_encoder(email_body)
    email = EmailSubscriptionDB(**obj_in_data)
    db.add(email)
    db.commit()
    db.refresh(email)
    return True
