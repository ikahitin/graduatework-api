from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

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
