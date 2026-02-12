from sqlalchemy import Column, Integer, String, TIMESTAMP, NUMERIC, Text
from sqlalchemy.sql import func
from .base import Base

class LedgerAccount(Base):
    """分类账模型 - 同时支持店铺账户和客户账户"""
    __tablename__ = "ledger_accounts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    code = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    type = Column(String(32), nullable=False)  # 收入账、成本账、预充值/会员账、临时账
    
    # 扩展字段：支持客户账户管理
    account_owner_id = Column(Integer, nullable=True, index=True)  # 账户所有者ID
    account_owner_type = Column(String(32), nullable=True)  # 账户所有者类型：shop, customer, member
    is_customer_account = Column(Integer, default=0)  # 0: 店铺账户, 1: 客户账户
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<LedgerAccount(id={self.id}, shop_id={self.shop_id}, name={self.name}, type={self.type}, is_customer_account={self.is_customer_account})>"

class LedgerEntry(Base):
    """账务分录模型 - 权威事实层，同时支持店铺账目和客户账户"""
    __tablename__ = "ledger_entries"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    account_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, nullable=True, index=True)
    event_id = Column(Integer, nullable=True, index=True)
    
    # 扩展字段：支持客户账户交易
    customer_id = Column(Integer, nullable=True, index=True)  # 关联的客户ID
    transaction_type = Column(String(32), nullable=False)  # 交易类型：sale, refund, cashback, redemption, etc.
    
    amount = Column(NUMERIC(12, 2), nullable=False)  # 精确到分
    direction = Column(String(8), nullable=False)  # IN 收入/增加，OUT 支出/减少
    description = Column(Text)
    
    # 扩展字段：为客户账户管理预留
    balance_before = Column(NUMERIC(12, 2), nullable=True)  # 交易前余额
    balance_after = Column(NUMERIC(12, 2), nullable=True)  # 交易后余额
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<LedgerEntry(id={self.id}, shop_id={self.shop_id}, account_id={self.account_id}, amount={self.amount}, direction={self.direction})>"