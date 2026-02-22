"""
Dot-Store V2.2 库存数据模型
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class Ingredient(Base):
    """
    食材模型 - 结构状态层
    """
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    unit = Column(String(16), nullable=False)
    current_stock = Column(Numeric(12, 2), nullable=False, default=0)
    min_stock = Column(Numeric(10, 2), default=0)
    cost_per_unit = Column(Numeric(10, 2), default=0)
    warning_stock = Column(Numeric(12, 2), nullable=False, default=0)
    category = Column(String(64), nullable=True)
    supplier = Column(String(128), nullable=True)
    expiry_date = Column(Date, nullable=True)
    status = Column(String(32), default='active')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Ingredient(id={self.id}, user_id={self.user_id}, name={self.name}, current_stock={self.current_stock})>"

    def is_low_stock(self) -> bool:
        """
        检查库存是否低于预警值
        """
        return self.current_stock < self.warning_stock


class StockRecord(Base):
    """
    库存记录模型
    """
    __tablename__ = "stock_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False, index=True)
    quantity = Column(Numeric(12, 2), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<StockRecord(id={self.id}, ingredient_id={self.ingredient_id}, type={self.type}, quantity={self.quantity})>"
