from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Float, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base
# from ..enums import ProductCategory



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    # is_available = Column(Boolean, default=True, nullable=False)
    ProductCategory = Column(Enum('grains', 'tubers', 'vegetables', 'fruits', 'livestock', 'cereals', 'oils', 'latex'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="products")
    
  
