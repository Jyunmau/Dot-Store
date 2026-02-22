"""
Dot-Store V2.2 订单数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base


class Order(Base):
    """
    订单模型 - 交易事实层
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    order_type = Column(String(32), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(32), nullable=True)
    customer_account_id = Column(Integer, nullable=True)
    cash_transaction_id = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey("order_categories.id"), nullable=True)
    tags = Column(JSONB, nullable=True)
    order_metadata = Column(JSONB, nullable=True)
    note = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="completed", index=True)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Order(id={self.id}, order_no={self.order_no}, amount={self.amount})>"

    def is_active(self) -> bool:
        """
        检查订单是否有效（未删除）
        """
        return not self.is_deleted


class OrderCategory(Base):
    """
    订单分类模型
    """
    __tablename__ = "order_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<OrderCategory(id={self.id}, user_id={self.user_id}, name={self.name})>"
