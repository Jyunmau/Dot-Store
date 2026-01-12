from sqlalchemy import Column, BigInteger, String, TIMESTAMP, NUMERIC, Text
from sqlalchemy.sql import func
from .base import Base

class LedgerAccount(Base):
    """分类账模型"""
    __tablename__ = "ledger_accounts"
    
    id = Column(BigInteger, primary_key=True, index=True)
    shop_id = Column(BigInteger, nullable=False, index=True)
    code = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    type = Column(String(32), nullable=False)  # 收入账、成本账、预充值/会员账、临时账
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<LedgerAccount(id={self.id}, shop_id={self.shop_id}, name={self.name}, type={self.type})>"

class LedgerEntry(Base):
    """账务分录模型 - 权威事实层"""
    __tablename__ = "ledger_entries"
    
    id = Column(BigInteger, primary_key=True, index=True)
    shop_id = Column(BigInteger, nullable=False, index=True)
    account_id = Column(BigInteger, nullable=False, index=True)
    order_id = Column(BigInteger, nullable=True, index=True)
    event_id = Column(BigInteger, nullable=True)
    amount = Column(NUMERIC(12, 2), nullable=False)  # 精确到分
    direction = Column(String(8), nullable=False)  # IN 收入，OUT 支出
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<LedgerEntry(id={self.id}, shop_id={self.shop_id}, amount={self.amount}, direction={self.direction})>"
