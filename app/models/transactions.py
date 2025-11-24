from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func, Float, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base 

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    payment = relationship("Payments", back_populates="transactions")
    order = relationship("Orders", back_populates="transactions")