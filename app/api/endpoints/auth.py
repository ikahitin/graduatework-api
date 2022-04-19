from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.api.utils import get_db, get_user_by_email
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security.auth import authenticate_user, create_access_token
from app.db import crud
from app.schemas.auth import Token, UserCreate, User, UserLogin

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user.__dict__}


@router.post("/signup", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
