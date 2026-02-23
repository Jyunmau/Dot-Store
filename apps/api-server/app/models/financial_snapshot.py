"""
Dot-Store V2.2 财务快照数据模型
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base


SNAPSHOT_TYPES = [
    ('daily', '每日快照'),
    ('monthly', '月度快照'),
    ('manual', '手动快照'),
]

VALIDATION_STATUS = [
    ('pending', '待校验'),
    ('passed', '校验通过'),
    ('failed', '校验失败'),
]


class FinancialSnapshot(Base):
    """
    财务快照模型 - 结构状态层
    每日财务状况的时间点视图
    """
    __tablename__ = "financial_snapshots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    snapshot_date = Column(Date, nullable=False, index=True)
    snapshot_type = Column(String(32), nullable=False, default='daily')
    cash_balance = Column(Numeric(12, 2), nullable=False, default=0)
    customer_prepaid = Column(Numeric(12, 2), nullable=False, default=0)
    inventory_value = Column(Numeric(12, 2), nullable=False, default=0)
    total_assets = Column(Numeric(12, 2), nullable=False, default=0)
    total_liabilities = Column(Numeric(12, 2), nullable=False, default=0)
    net_assets = Column(Numeric(12, 2), nullable=False, default=0)
    daily_revenue = Column(Numeric(12, 2), nullable=False, default=0)
    daily_expense = Column(Numeric(12, 2), nullable=False, default=0)
    daily_profit = Column(Numeric(12, 2), nullable=False, default=0)
    order_count = Column(Integer, nullable=False, default=0)
    validation_status = Column(String(32), nullable=False, default='pending')
    validation_errors = Column(JSONB, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<FinancialSnapshot(id={self.id}, date={self.snapshot_date}, net_assets={self.net_assets})>"

    def calculate_totals(self):
        """
        计算总资产和净资产
        """
        self.total_assets = self.cash_balance + self.inventory_value
        self.total_liabilities = self.customer_prepaid
        self.net_assets = self.total_assets - self.total_liabilities
        self.daily_profit = self.daily_revenue - self.daily_expense
