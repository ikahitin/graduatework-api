from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils import get_db
from app.core.security.auth import get_current_user
from app.db import crud
from app.schemas.apartment import ApartmentReservation
from app.schemas.auth import User
from app.schemas.car import CarReservation
from app.schemas.general import ReservationStatusEnum, ReservationTypeEnum, EmailSubscription
from app.schemas.taxi import TaxiReservation

router = APIRouter()


@router.get("/reservation", response_model=List[Union[ApartmentReservation, CarReservation, TaxiReservation]])
async def get_reservations(reservation_status: ReservationStatusEnum, reservation_type: ReservationTypeEnum,
                           db: Session = Depends(get_db), current_user: User = Depends(get_current_user), ):
    reservations = crud.get_reservations(db, current_user.email, reservation_status, reservation_type)
    return reservations


@router.post("/subscribe-email")
async def subscribe_email(email_body: EmailSubscription, db: Session = Depends(get_db)):
    email_added = crud.add_email(db, email_body)
    return email_added
