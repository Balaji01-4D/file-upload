from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, FLOAT

from src.database.core import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, unique=True, nullable=False)
    password = Column(VARCHAR, nullable=False)

    files = relationship('File', back_populates='user')
