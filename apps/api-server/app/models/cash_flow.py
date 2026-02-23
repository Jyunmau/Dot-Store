"""
Dot-Store V2.2 现金流分析数据模型
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base


ANALYSIS_TYPES = [
    ('daily', '每日分析'),
    ('weekly', '每周分析'),
    ('monthly', '每月分析'),
    ('quarterly', '每季分析'),
    ('yearly', '每年分析'),
]

RISK_LEVELS = [
    ('low', '低风险'),
    ('medium', '中风险'),
    ('high', '高风险'),
    ('critical', '严重风险'),
]


class CashFlowAnalysis(Base):
    """
    现金流分析模型 - 分析结果层
    存储周期性现金流分析结果
    """
    __tablename__ = "cash_flow_analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    analysis_date = Column(Date, nullable=False, index=True)
    analysis_type = Column(String(32), nullable=False, default='monthly')
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    total_income = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    total_expense = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    net_cash_flow = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    avg_daily_income = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    avg_daily_expense = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    
    income_structure = Column(JSONB, nullable=False, default=dict)
    expense_structure = Column(JSONB, nullable=False, default=dict)
    
    health_score = Column(Numeric(5, 2), nullable=False, default=Decimal('0'))
    risk_level = Column(String(32), nullable=False, default='low')
    recommendations = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<CashFlowAnalysis(id={self.id}, period={self.period_start}~{self.period_end})>"

    def calculate_net_flow(self):
        """
        计算净现金流
        """
        self.net_cash_flow = self.total_income - self.total_expense


class CashFlowForecast(Base):
    """
    现金流预测模型 - 预测结果层
    存储未来现金流预测数据
    """
    __tablename__ = "cash_flow_forecasts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    forecast_date = Column(Date, nullable=False, index=True)
    target_date = Column(Date, nullable=False, index=True)
    
    predicted_income = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    predicted_expense = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    predicted_balance = Column(Numeric(12, 2), nullable=False, default=Decimal('0'))
    confidence_level = Column(Numeric(5, 2), nullable=False, default=Decimal('0'))
    
    risk_alert = Column(Boolean, nullable=False, default=False)
    alert_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<CashFlowForecast(id={self.id}, target={self.target_date}, balance={self.predicted_balance})>"


class RiskAlert(Base):
    """
    风险预警模型 - 预警信息层
    存储现金流风险预警信息
    """
    __tablename__ = "risk_alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    alert_date = Column(Date, nullable=False, index=True)
    alert_level = Column(String(32), nullable=False, index=True)
    alert_type = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    suggestions = Column(JSONB, nullable=True)
    is_read = Column(Boolean, nullable=False, default=False)
    is_resolved = Column(Boolean, nullable=False, default=False)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<RiskAlert(id={self.id}, level={self.alert_level}, type={self.alert_type})>"
