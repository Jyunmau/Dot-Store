"""
Dot-Store V2.2 支付记录模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class Payment(Base):
    """
    支付记录模型
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_method = Column(String(32), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    note = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, method={self.payment_method})>"
