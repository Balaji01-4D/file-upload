from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.crud.user import create_user

from app.models import User
from app.schemas.user import UserCreate, UserResponse

userRouter = APIRouter()

@userRouter.post("", response_model=UserResponse)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="email already existed")
    new_user = await create_user(db, user)
    return new_user
