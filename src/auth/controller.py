import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.core import get_db
from src.users.models import User
from . import service
from . import models

authRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@authRouter.post("/register", response_model=models.UserResponse)
async def register_user(user: models.UserCreate, db: AsyncSession = Depends(get_db)):
    is_user_exist = await service.get_user_by_email(db, user.email)
    if is_user_exist:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="email already existed")

    new_user = await service.create_user(db, user)
    return new_user

@authRouter.post("/token", response_model=models.Token)
async def login_user_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = await service.authenticate_user(db, form_data)
    return service.create_access_token(user.id, user.email)

@authRouter.get("/me", response_model=models.UserResponse)
async def me(token: str = Depends(oauth2_scheme)):
    email = service.verify_token(token)
    user = await service.get_user_by_email(db, email)

    return user
