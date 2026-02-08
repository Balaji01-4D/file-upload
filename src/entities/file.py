from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, FLOAT, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
import uuid

from src.database.core import Base

class File(Base):
    __tablename__ = 'file'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR, nullable=False)
    size = Column(FLOAT, nullable=False)
    type = Column(VARCHAR)
    path = Column(VARCHAR, nullable=False)
    owner = Column(UUID, ForeignKey('user.id'), nullable=False)
    added_at = Column(TIMESTAMP, nullable=False, default=datetime.now)

    user = relationship("User", back_populates="files")
