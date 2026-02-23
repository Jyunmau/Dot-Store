"""
Dot-Store V2.2 现金账户数据模型
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base


class CashAccount(Base):
    """
    现金账户模型 - 结构状态层
    管理店铺现金账户、现金收支记录和账户余额追踪
    """
    __tablename__ = "cash_accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    account_name = Column(String(64), nullable=False)
    account_type = Column(String(32), nullable=False, default="cash")
    balance = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    total_income = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    total_expense = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    status = Column(String(32), nullable=False, default="active", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, nullable=False, default=0)

    transactions = relationship("CashTransaction", back_populates="account")

    def __repr__(self):
        return f"<CashAccount(id={self.id}, account_name={self.account_name}, balance={self.balance})>"

    def is_active(self) -> bool:
        """
        检查账户是否有效
        """
        return self.status == "active"


class CashTransaction(Base):
    """
    现金交易模型 - 交易事实层
    不可变的交易记录，所有收支记录
    """
    __tablename__ = "cash_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("cash_accounts.id"), nullable=False, index=True)
    transaction_no = Column(String(32), unique=True, nullable=False, index=True)
    transaction_type = Column(String(32), nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    balance_before = Column(Numeric(12, 2), nullable=False)
    balance_after = Column(Numeric(12, 2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    customer_transaction_id = Column(Integer, ForeignKey("customer_transactions.id"), nullable=True)
    note = Column(Text, nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    account = relationship("CashAccount", back_populates="transactions")

    def __repr__(self):
        return f"<CashTransaction(id={self.id}, transaction_no={self.transaction_no}, amount={self.amount})>"


class CashTransactionType(str, Enum):
    """
    现金交易类型枚举
    """
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER_IN = 'transfer_in'
    TRANSFER_OUT = 'transfer_out'
    ADJUST_ADD = 'adjust_add'
    ADJUST_SUB = 'adjust_sub'


INCOME_CATEGORIES = [
    ('order_income', '订单收入'),
    ('recharge_income', '充值收入'),
    ('refund_income', '退款收入'),
    ('other_income', '其他收入'),
]

EXPENSE_CATEGORIES = [
    ('purchase', '采购支出'),
    ('salary', '工资支出'),
    ('rent', '房租支出'),
    ('utility', '水电费'),
    ('other_expense', '其他支出'),
]
