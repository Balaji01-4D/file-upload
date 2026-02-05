from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class File(BaseModel):
    id: UUID | None = None
    name: str
    size: float
    type: str | None = None
    owner: UUID
    added_at: datetime | None

    class Config:
        orm_mode = True