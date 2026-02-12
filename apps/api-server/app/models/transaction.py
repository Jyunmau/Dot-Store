"""
Dot-Store V2.1 收支记录数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class Transaction(Base):
    """
    收支记录模型
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(32), nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    note = Column(Text, nullable=True)
    attachment_url = Column(String(256), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, type={self.type}, amount={self.amount})>"

    def is_income(self) -> bool:
        """
        检查是否为收入记录
        """
        return self.type == "income"

    def is_expense(self) -> bool:
        """
        检查是否为支出记录
        """
        return self.type == "expense"


class TransactionCategory(Base):
    """
    收支分类模型
    """
    __tablename__ = "transaction_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    type = Column(String(32), nullable=False, index=True)
    description = Column(String(256), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TransactionCategory(id={self.id}, user_id={self.user_id}, name={self.name}, type={self.type})>"

    def is_income_category(self) -> bool:
        """
        检查是否为收入分类
        """
        return self.type == "income"

    def is_expense_category(self) -> bool:
        """
        检查是否为支出分类
        """
        return self.type == "expense"
