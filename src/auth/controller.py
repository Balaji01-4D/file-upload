from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.core import get_db
from src.users.models import User
from . import service
from . import models

userRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@userRouter.post("/register", response_model=UserResponse)
async def register_user(user: models.UserCreate, db: AsyncSession = Depends(get_db)):
    is_user_exist = service.check_user_exists(db, user.email)
    if is_user_exist:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="email already existed")

    new_user = await service.create_user(db, user)
    return new_user

@userRouter.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):

    if not logined_user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="user not found")
