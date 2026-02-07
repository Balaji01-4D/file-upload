from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class File(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID | None = None
    name: str
    size: float
    type: str | None = None
    owner: UUID
    added_at: datetime | None = None