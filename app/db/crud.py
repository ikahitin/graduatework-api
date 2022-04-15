from sqlalchemy.orm import Session

from app.core.security.auth import get_password_hash
from app.db.models.user import User
from app.schemas.auth import UserCreate


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
