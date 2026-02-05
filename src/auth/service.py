import os
import jwt
from uuid import UUID
from datetime import timedelta, timezone, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models
from src.users.models import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30
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


async def check_user_exists(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def authenticate_user(db: AsyncSession, user_login_request: models.UserLogin) -> User | bool:
    stmt = select(User).where(User.email == user_login_request.email)
    result = await db.execute(stmt)

    db_user = result.scalars().first()
    if not db_user and not check_password(db_user.password, user_login_request.password):
        return False
    return db_user

async def create_access_token(user_id: UUID, email: str, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': user_id,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, os.getenv('JWT_SECRET'), algorithm=JWT_ALGORITHM)


