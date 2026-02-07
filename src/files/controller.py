from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, service
from src.auth.service import verify_token, get_user_by_email
from src.auth.controller import oauth2_scheme
from src.database.core import get_db


file_router = APIRouter(
    prefix="/uploads",
    tags=["uploads"]
)

uploads = Path("uploads")
uploads.mkdir(exist_ok=True)

@file_router.post("/", response_model=models.File)
async def upload_file(file: UploadFile, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    filename = file.filename
    ext = Path(filename).suffix

    user_email = await verify_token(token)
    user = await get_user_by_email(db, user_email)

    local_file_path = uploads / f"{user.id}-{filename}"

    try:
        with open(local_file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)
    except:
        raise HTTPException(status_code=status.WS_1003_UNSUPPORTED_DATA, detail="failed to read the data")

    file_model = models.File(name=file.filename, size=file.size, type=file.content_type, owner=user.id)
    return await service.save_file(db, file_model)


@file_router.get("/", response_model=list[models.File])
async def get_files(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_email = await verify_token(token)
    user = await get_user_by_email(db, user_email)

    return await service.get_file(db, user.id)


        