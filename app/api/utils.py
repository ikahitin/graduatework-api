import datetime
import os
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.boto3.client import client
from app.db.models.user import User
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
