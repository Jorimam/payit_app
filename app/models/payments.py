from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Float, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base 

class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    transaction_id = Column(String(100), nullable=False, unique=True)
    amount = Column(DECIMAL(10,2), nullable=False)
    payment_type = Column(String(50), nullable=False)
    payment_gateway = Column(String(50), nullable=False)
    payload = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Orders", back_populates="payments")
    transaction = relationship("Transactions", back_populates="payment") 