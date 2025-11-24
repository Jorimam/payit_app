from sqlalchemy import Integer, Column, String, DateTime, Enum, func, ForeignKey
from .base import Base
from ..enums import Gender, Category
from sqlalchemy.orm import relationship
from .user import User

class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)

user = relationship("User", back_populates="buyer")

