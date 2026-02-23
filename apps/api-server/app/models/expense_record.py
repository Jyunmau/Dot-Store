"""
Dot-Store V2.2 成本记录数据模型
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base


EXPENSE_CATEGORIES = [
    ('rent', '房租'),
    ('labor', '人工'),
    ('utilities', '水电'),
    ('marketing', '营销'),
    ('finance', '财务'),
    ('maintenance', '维护'),
    ('supplies', '耗材'),
    ('other', '其他'),
]

COST_BEHAVIORS = [
    ('fixed', '固定成本'),
    ('variable', '变动成本'),
    ('semi_variable', '半变动成本'),
]

COST_FUNCTIONS = [
    ('operating', '运营成本'),
    ('administrative', '管理成本'),
    ('sales', '销售成本'),
]


class ExpenseRecord(Base):
    """
    成本记录模型 - 交易事实层
    """
    __tablename__ = "expense_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(Text, nullable=True)
    expense_date = Column(Date, nullable=False, index=True)
    cost_behavior = Column(String(32), nullable=True)
    cost_function = Column(String(32), nullable=True)
    extra_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ExpenseRecord(id={self.id}, category={self.category}, amount={self.amount})>"
