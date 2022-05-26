from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils import get_db
from app.core.security.auth import get_current_user
from app.db import crud
from app.schemas.apartment import ApartmentReservation
from app.schemas.auth import User
from app.schemas.car import CarReservation
from app.schemas.general import ReservationStatusEnum, ReservationTypeEnum

router = APIRouter()


@router.get("/reservation", response_model=List[Union[ApartmentReservation, CarReservation]])
async def get_reservations(reservation_status: ReservationStatusEnum, reservation_type: ReservationTypeEnum, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),):
    reservations = crud.get_reservations(db, current_user.email, reservation_status, reservation_type)
    return reservations
