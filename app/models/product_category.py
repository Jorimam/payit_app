from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Float, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base
from ..enums import ProductCategoryEnum
from sqlalchemy.types import Enum as SqlEnum

class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(SqlEnum(ProductCategoryEnum), nullable=False, index=True)

    products = relationship("Product", back_populates="category", cascade="all, delete")