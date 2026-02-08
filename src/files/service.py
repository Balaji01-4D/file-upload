import os
import logging
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from . import models
from src.entities.file import File

logger = logging.getLogger(__file__)


async def save_file(db: AsyncSession, file: models.File) -> File:
    db_file = File(name=file.name, size=file.size, type=file.type, owner=file.owner, path=file.path)
    try:
        db.add(db_file)
        await db.commit()
        await db.refresh(db_file)
        return db_file
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="failed to upload the file")

async def delete_file(db: AsyncSession, file_id: UUID, user_id: UUID):
    try:
        stmt = select(File).where(File.id == file_id, File.owner == user_id)
        result = await db.execute(stmt)
        file_obj: File | None = result.scalar_one_or_none()

        if file_obj is None:
            logger.exception("failed to get the file record")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file not found")

        file_path = file_obj.path

        await db.delete(file_obj)
        await db.commit()

    except SQLAlchemyError as e:
        logger.exception("failed to delete the file record", e._message)
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e._message) from e

    try:
        os.remove(file_path)
    except FileNotFoundError:
        logger.warning("file is missing from path")
    except OSError as os_err:
        logger.exception("failed to delete the file", os_err.strerror)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="failed to delete the file from server") from e


async def get_file(db: AsyncSession, owner_id: UUID):
    stmt = select(File).where(File.owner == owner_id)
    result = await db.execute(stmt)

    return result.scalars().all()