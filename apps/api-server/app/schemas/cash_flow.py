"""
Dot-Store V2.2 现金流分析Schema
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class SafetyIndexResponse(BaseModel):
    """三色安全指数响应"""
    model_config = ConfigDict(from_attributes=True)
    
    safety_score: float = Field(..., description="安全指数分数(0-100)")
    safety_level: str = Field(..., description="安全等级: safe/warning/danger")
    color_code: str = Field(..., description="颜色代码")
    message: str = Field(..., description="用户友好提示语")
    factors: Dict[str, Any] = Field(..., description="计算因素")


class CashFlowForecastResponse(BaseModel):
    """现金流预测响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    forecast_date: date
    target_date: date
    predicted_income: Decimal
    predicted_expense: Decimal
    predicted_balance: Decimal
    confidence_level: Decimal
    risk_alert: bool
    alert_message: Optional[str] = None
    created_at: datetime


class CashFlowForecastListResponse(BaseModel):
    """现金流预测列表响应"""
    items: List[CashFlowForecastResponse]
    total: int


class IncomeStructureResponse(BaseModel):
    """收入结构分析响应"""
    total_income: Decimal = Field(..., description="总收入")
    income_by_category: Dict[str, Decimal] = Field(..., description="按分类的收入")
    income_by_mode: Dict[str, Decimal] = Field(..., description="按模式的收入")
    income_trend: List[Dict[str, Any]] = Field(..., description="收入趋势")
    stability_score: float = Field(..., description="收入稳定性评分")
    growth_rate: Optional[float] = Field(None, description="收入增长率")


class ExpenseStructureResponse(BaseModel):
    """成本结构分析响应"""
    total_expense: Decimal = Field(..., description="总支出")
    expense_by_category: Dict[str, Decimal] = Field(..., description="按分类的支出")
    expense_by_behavior: Dict[str, Decimal] = Field(..., description="按行为分类的支出")
    expense_by_function: Dict[str, Decimal] = Field(..., description="按功能分类的支出")
    expense_trend: List[Dict[str, Any]] = Field(..., description="支出趋势")
    anomaly_detected: bool = Field(..., description="是否检测到异常")


class BreakEvenAnalysisResponse(BaseModel):
    """盈亏平衡分析响应"""
    break_even_point: Decimal = Field(..., description="盈亏平衡点(销售额)")
    current_revenue: Decimal = Field(..., description="当前收入")
    fixed_cost: Decimal = Field(..., description="固定成本")
    variable_cost_ratio: float = Field(..., description="变动成本比率")
    contribution_margin_ratio: float = Field(..., description="边际贡献率")
    safety_margin: Decimal = Field(..., description="安全边际")
    safety_margin_ratio: float = Field(..., description="安全边际率")
    status: str = Field(..., description="状态: profit/loss/break_even")


class CashFlowAnalysisResponse(BaseModel):
    """现金流分析响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    analysis_date: date
    analysis_type: str
    period_start: date
    period_end: date
    total_income: Decimal
    total_expense: Decimal
    net_cash_flow: Decimal
    avg_daily_income: Decimal
    avg_daily_expense: Decimal
    income_structure: Dict[str, Any]
    expense_structure: Dict[str, Any]
    health_score: Decimal
    risk_level: str
    recommendations: Optional[List[str]] = None
    created_at: datetime


class MonthlyReportResponse(BaseModel):
    """月度健康报告响应"""
    year: int
    month: int
    period_start: date
    period_end: date
    
    total_income: Decimal
    total_expense: Decimal
    net_cash_flow: Decimal
    
    income_structure: IncomeStructureResponse
    expense_structure: ExpenseStructureResponse
    break_even: BreakEvenAnalysisResponse
    safety_index: SafetyIndexResponse
    
    health_score: float
    risk_level: str
    
    recommendations: List[str]
    action_items: List[str]
    
    comparison: Optional[Dict[str, Any]] = None


class IncomeVolatilityResponse(BaseModel):
    """收入波动归因响应"""
    volatility_score: float = Field(..., description="波动性评分")
    trend: str = Field(..., description="趋势: up/down/stable")
    change_percentage: float = Field(..., description="变化百分比")
    
    factors: List[Dict[str, Any]] = Field(..., description="影响因素")
    main_cause: str = Field(..., description="主要原因")
    
    suggestions: List[str] = Field(..., description="优化建议")


class CashFlowAnalyzeRequest(BaseModel):
    """现金流分析请求"""
    period_start: date = Field(..., description="分析周期开始日期")
    period_end: date = Field(..., description="分析周期结束日期")
    analysis_type: str = Field(default="monthly", description="分析类型")


class DashboardResponse(BaseModel):
    """仪表盘响应"""
    safety_index: SafetyIndexResponse = Field(..., description="安全指数")
    current_balance: Decimal = Field(..., description="当前余额")
    yesterday_change: Decimal = Field(..., description="昨日变动")
    monthly_income: Decimal = Field(..., description="本月收入")
    monthly_expense: Decimal = Field(..., description="本月支出")
    monthly_profit: Decimal = Field(..., description="本月利润")
    recent_trend: List[Dict[str, Any]] = Field(..., description="近期趋势")
    active_alerts: List[Dict[str, Any]] = Field(..., description="活跃预警")
    forecast_summary: Dict[str, Any] = Field(..., description="预测摘要")
