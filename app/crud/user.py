from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from hashlib import sha256
from app.core.security import hash_password

async def create_user(db: AsyncSession, user: UserCreate):
    hassed_password = hash_password(user.password.encode('utf-8'))

    db_user = User(name=user.name, email=user.email, password=hassed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = db.execute(
        select(User).wh
        )
