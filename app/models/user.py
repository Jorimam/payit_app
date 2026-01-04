from sqlalchemy import Integer, Column, String, DateTime, Enum, func, ForeignKey
from .base import Base
from ..enums import Gender
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(30), min_length=3, max_length=30, nullable=False)
    # lname = Column(String(30), min_length=3, max_length=30, nullable=True)
    phone = Column(String(20), unique=True, min_length=11, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False) #assignment, set boundaries
    gender = Column(Enum(Gender.male.value, Gender.female.value), nullable=False) # create Enum
    location = Column(String(255), min_length=3, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # products = relationship("Product", back_populates="user", cascade="all, delete")
    # buyer = relationship("Buyer", back_populates="user", uselist=False, cascade="all, delete")
    # farmer = relationship("Farmer", back_populates="user", uselist=False, cascade="all, delete")
