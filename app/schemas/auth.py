from typing import Optional

from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserBase

