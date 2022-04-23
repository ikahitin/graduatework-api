import os
import uuid

import aiofiles
from fastapi import HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import BASEDIR
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
    img_dir = os.path.join(BASEDIR, f'static/{img_folder}')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)
    return file_name


async def apartment_params(city: str, start: str, end: str, adults: int, children: int, rooms: int):
    return {"city": city, "start": start, "end": end, "adults": adults, "children": children, "rooms": rooms}
