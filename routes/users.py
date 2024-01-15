from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, database
from sqlalchemy.orm import Session

from models.users import User
from functions.users import all_users, update_user, create_user
from schemas.users import UserCreate, UserUpdate

Base.metadata.create_all(bind=engine)

router_user = APIRouter()


@router_user.post('/create', )
def add_user(form: UserCreate,
             db: Session = Depends(database)):
    if create_user(form, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_user.get('/', status_code=200)
def get_users(search: str = None, is_active: bool = True, user_id: int = 0, role: str = None, page: int = 1, limit: int = 25,
              db: Session = Depends(database)):
    if user_id:
        return db.query(User).filter_by(id=user_id, is_active=True).first()
    else:
        return all_users(search, is_active, role, page, limit, db)


@router_user.put("/update")
def user_update(form: UserUpdate, db: Session = Depends(database)):
    if update_user(form, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")
