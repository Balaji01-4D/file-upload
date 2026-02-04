from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Base = declarative_base()

def get_db_url():
    return os.getenv("DATABASE_URL")

engine = create_async_engine(get_db_url(), echo=True)

SessionLocal = async_sessionmaker(autoflush=False, class_=AsyncSession, bind=engine, expire_on_commit=False) 

async def get_db():
    async with SessionLocal() as db:
        yield db
