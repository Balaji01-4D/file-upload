from pydantic import BaseModel, ConfigDict
import uuid

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID | None = None
    name: str
    email: str
    password: str


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str
