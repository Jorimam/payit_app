from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Float, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base
from .farmers import Farmer


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("product_category.id"), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    farmer = relationship("Farmer", back_populates="products", cascade="all, delete")
    category = relationship("ProductCategory", back_populates="products", cascade="all, delete")
 