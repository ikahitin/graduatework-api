import datetime
import os
import uuid
from math import sin, cos, sqrt, atan2, radians

from fastapi import HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.boto3.client import client
from app.db.models.user import User
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
R = 6373.0


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def save_image(file: UploadFile, img_folder: str):
    _, ext = os.path.splitext(file.filename)
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    content = await file.read()
    client.put_object(
        Bucket='graduate-static',
        Key=f'{img_folder}/{file_name}',
        Body=content,
        ContentType=f'image/{ext}'
    )
    return file_name


async def apartment_params(city: str, start: datetime.date, end: datetime.date, adults: int, children: int):
    return {"city": city, "start": start, "end": end, "adults": adults, "children": children}


async def location_params(start_latitude: float, start_longitude: float, end_latitude: float, end_longitude: float):
    return {"start_latitude": start_latitude, "start_longitude": start_longitude, "end_latitude": end_latitude,
            "end_longitude": end_longitude}


def calc_distance(start_lat, start_lng, end_lat, end_lng):
    lat1 = radians(start_lat)
    lon1 = radians(start_lng)
    lat2 = radians(end_lat)
    lon2 = radians(end_lng)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def add_price_obj(db_obj, location_details):
    obj = db_obj.__dict__
    dist = calc_distance(start_lat=location_details.get('start_latitude'),
                         start_lng=location_details.get('start_longitude'),
                         end_lat=location_details.get('end_latitude'),
                         end_lng=location_details.get('end_longitude'))
    price = dist * db_obj.price_for_km
    obj["price_for_ride"] = int(price)
    return obj


def calc_price_in_taxi_query(query, location_details):
    query_list = []
    for i in query.all():
        obj = add_price_obj(i, location_details)
        query_list.append(obj)
    sorted_list = sorted(query_list, key=lambda d: d['price_for_ride'])
    return sorted_list
