"""
Dot-Store V2.2 客户账户数据模型
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base


class CustomerAccount(Base):
    """
    客户账户模型 - 结构状态层
    管理客户预付款账户、预收权益负债追踪和客户消费记录
    """
    __tablename__ = "customer_accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    customer_name = Column(String(64), nullable=False)
    phone = Column(String(32), nullable=False, index=True)
    balance = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    total_recharged = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    total_consumed = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    status = Column(String(32), nullable=False, default="active", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, nullable=False, default=0)

    transactions = relationship("CustomerTransaction", back_populates="account")

    def __repr__(self):
        return f"<CustomerAccount(id={self.id}, customer_name={self.customer_name}, balance={self.balance})>"

    def is_active(self) -> bool:
        """
        检查账户是否有效
        """
        return self.status == "active"


class CustomerTransaction(Base):
    """
    客户交易模型 - 交易事实层
    不可变的交易记录，所有充值和消费记录
    """
    __tablename__ = "customer_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("customer_accounts.id"), nullable=False, index=True)
    transaction_no = Column(String(32), unique=True, nullable=False, index=True)
    transaction_type = Column(String(32), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    balance_before = Column(Numeric(12, 2), nullable=False)
    balance_after = Column(Numeric(12, 2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    note = Column(Text, nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    account = relationship("CustomerAccount", back_populates="transactions")

    def __repr__(self):
        return f"<CustomerTransaction(id={self.id}, transaction_no={self.transaction_no}, amount={self.amount})>"


class TransactionType(str, Enum):
    """
    客户交易类型枚举
    """
    RECHARGE = 'recharge'
    CONSUME = 'consume'
    REFUND = 'refund'
    ADJUST_ADD = 'adjust_add'
    ADJUST_SUB = 'adjust_sub'
