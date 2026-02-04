from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from hashlib import sha256

async def create_user(db: AsyncSession, user: UserCreate):
    hassed_password = sha256(user.password.encode('utf-8')).hexdigest()

    db_user = User(name=user.name, email=user.email, password=hassed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user
