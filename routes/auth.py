from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from db import get_db
from schemas.users import UserCurrent
from models.models import Users
import os
from dotenv import load_dotenv
from utils.commands import credentials_exception, INCORRECT_PASS, NOT_FOUND

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

login_router = APIRouter(prefix='/auth', tags=['User auth section'],)


def hash_password(password):
    return pwd_context.hash(password)


async def access_token_create(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def current_user(db: Session = get_db, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Users).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    return user


async def current_active_user(user: UserCurrent = Depends(current_user)):
    if user.is_active:
        return user
    raise HTTPException(status_code=400, detail="The user is inactive")


async def get_current_user_socket(websocket: WebSocket, db: Session = get_db):
    try:
        token = websocket.query_params.get("token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Users).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    return user


@login_router.post("/token/")
async def login_for_access_token(db: Session = get_db, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).filter_by(username=form_data.username, is_active=True).first()
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password)
        if not is_validate_password:
            raise INCORRECT_PASS
    else:
        raise NOT_FOUND
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await access_token_create(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    db.query(Users).filter_by(username=form_data.username).update({
        Users.token: access_token
    })
    db.commit()
    return {'id': user.id, "access_token": access_token, "role": user.role}
