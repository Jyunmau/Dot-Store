"""
Dot-Store V2.2 库存流水模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class StockTransaction(Base):
    """
    库存流水模型 - 交易事实层
    """
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    transaction_no = Column(String(32), unique=True, nullable=False)
    transaction_type = Column(String(32), nullable=False, index=True)
    quantity = Column(Numeric(10, 2), nullable=False)
    stock_before = Column(Numeric(10, 2), nullable=False)
    stock_after = Column(Numeric(10, 2), nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=True)
    total_cost = Column(Numeric(12, 2), nullable=True)
    note = Column(Text, nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<StockTransaction(id={self.id}, no={self.transaction_no}, type={self.transaction_type})>"
