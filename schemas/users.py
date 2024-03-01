from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from db import SessionLocal

db: Session = SessionLocal()


class UserBase(BaseModel):
    username: str
    role: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    is_active: bool = True


class UserUpdate(BaseModel):
    user_id: int
    username: str
    password: str
    role: str
    is_active: bool


class UserCurrent(BaseModel):
    id: int
    username: str
    password: str
    role: str
    is_active: bool
