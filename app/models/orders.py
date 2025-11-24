from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Float, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base
# from ..enums import ProductCategory

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    total_price = Column(DECIMAL(10,2), nullable=False)
    order_status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    buyer = relationship("Buyer", back_populates="orders")
    product = relationship("Product", back_populates="orders")