from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID

from . import models

from src.entities.file import File

async def save_file(db: AsyncSession, file: models.File) -> File:
    db_file = File(name=file.name, size=file.size, type=file.type, owner=file.owner)
    try:
        db.add(db_file)
        await db.commit()
        await db.refresh(db_file)
        return db_file
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="failed to upload the file")


async def get_file(db: AsyncSession, owner_id: UUID):
    stmt = select(File).where(File.owner == owner_id)
    result = await db.execute(stmt)

    return result.scalars().all()



        
