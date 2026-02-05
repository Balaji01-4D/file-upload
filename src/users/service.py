from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from hashlib import sha256
from app.core.security import hash_password



async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = db.execute(
        select(User).wh
        )
