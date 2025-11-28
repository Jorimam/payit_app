from sqlalchemy import Integer, Column, String, DateTime, Enum, func, ForeignKey
from .base import Base
from ..enums import Gender
from sqlalchemy.orm import relationship
from .user import User

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

user = relationship("User", back_populates="buyer")

