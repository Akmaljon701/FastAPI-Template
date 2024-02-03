from fastapi import APIRouter, Depends, HTTPException
from db import database
from sqlalchemy.orm import Session
from models.users import Users
from functions.users import all_users, update_user, create_user
from routes.auth import current_active_user
from schemas.users import UserCreate, UserUpdate, UserCurrent

router_user = APIRouter(prefix='/user', tags=['User apis'])


@router_user.post('/create', )
async def add_user(form: UserCreate,
                   db: Session = Depends(database)):
    if await create_user(form, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_user.get('/', status_code=200)
async def get_users(search: str = None, is_active: bool = True, user_id: int = 0, role: str = None, page: int = 1,
                    limit: int = 25,
                    db: Session = Depends(database)):
    if user_id:
        return db.query(Users).filter_by(id=user_id, is_active=True).first()
    else:
        return await all_users(search, is_active, role, page, limit, db)


@router_user.put("/update")
async def user_update(form: UserUpdate, db: Session = Depends(database)):
    if await update_user(form, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")


@router_user.get("/current_active")
async def get_current_active_user(user: UserCurrent = Depends(current_active_user)):
    return user
