import os
import jwt
from uuid import UUID
from typing import Annotated
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import models
from src.entities import User

ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(weeks=2)
JWT_ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def check_password(hashed_pw: str, plain_pw: str) -> bool:
    return bcrypt_context.verify(plain_pw, hashed_pw)

async def create_user(db: AsyncSession, user: models.UserCreate):
    db_user = User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, user_login_form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> User | bool:
    stmt = select(User).where(User.email == user_login_form.username)
    result = await db.execute(stmt)

    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    if not check_password(db_user.password, user_login_form.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password wrong")
    return db_user

async def create_access_token(user_id: UUID, email: str, expires_delta: timedelta | None = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    encode = {
        'sub': email,
        'id': user_id,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, os.getenv('JWT_SECRET'), algorithm=JWT_ALGORITHM)

async def verify_token(token: str) -> str:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials")
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=JWT_ALGORITHM)
        user_email: str = payload.get('sub')
        if user_email is None:
            raise credentials_exception

        return user_email
    except jwt.PyJWTError:
        raise credentials_exception
