"""
Dot-Store V2.2 现金流分析API路由
"""
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.cash_flow import (
    SafetyIndexResponse,
    CashFlowAnalysisResponse,
    CashFlowForecastResponse,
    CashFlowForecastListResponse,
    IncomeStructureResponse,
    ExpenseStructureResponse,
    BreakEvenAnalysisResponse,
    MonthlyReportResponse,
    IncomeVolatilityResponse,
    DashboardResponse,
    CashFlowAnalyzeRequest,
)
from app.schemas.risk_alert import RiskAlertResponse, RiskAlertListResponse
from app.services.cash_flow_service import CashFlowService
from app.models.user import User

router = APIRouter(prefix="/cashflow", tags=["现金流分析"])


@router.get("/safety-index", response_model=SafetyIndexResponse, summary="获取三色安全指数")
async def get_safety_index(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取三色安全指数
    
    - 基于现金余额、预收款负债、日均支出计算
    - 返回安全分数(0-100)和等级(safe/warning/danger)
    - 提供状态描述和建议
    """
    result = CashFlowService.calculate_safety_index(db, current_user.id)
    return SafetyIndexResponse(**result)


@router.post("/analyze", response_model=CashFlowAnalysisResponse, summary="执行现金流分析")
async def analyze_cash_flow(
    request: CashFlowAnalyzeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    执行现金流分析
    
    - 分析指定周期的收支情况
    - 计算收入结构和支出结构
    - 评估健康度评分和风险等级
    - 生成经营建议
    """
    analysis = CashFlowService.analyze_cash_flow(
        db=db,
        user_id=current_user.id,
        period_start=request.period_start,
        period_end=request.period_end,
        analysis_type=request.analysis_type
    )
    return CashFlowAnalysisResponse.model_validate(analysis)


@router.get("/forecast", response_model=CashFlowForecastListResponse, summary="获取现金流预测")
async def get_forecast(
    days: int = Query(30, ge=7, le=90, description="预测天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取现金流预测
    
    - 基于历史数据预测未来现金流
    - 使用移动平均法计算
    - 提供置信度和风险预警
    """
    forecasts = CashFlowService.forecast_cash_flow(
        db=db,
        user_id=current_user.id,
        days=days
    )
    
    return CashFlowForecastListResponse(
        items=[CashFlowForecastResponse.model_validate(f) for f in forecasts],
        total=len(forecasts)
    )


@router.get("/income-structure", response_model=IncomeStructureResponse, summary="获取收入结构分析")
async def get_income_structure(
    period_start: date = Query(..., description="周期开始日期"),
    period_end: date = Query(..., description="周期结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取收入结构分析
    
    - 按分类统计收入
    - 计算各分类占比
    - 支持自定义时间范围
    """
    result = CashFlowService.get_income_structure(
        db=db,
        user_id=current_user.id,
        period_start=period_start,
        period_end=period_end
    )
    
    return IncomeStructureResponse(**result)


@router.get("/expense-structure", response_model=ExpenseStructureResponse, summary="获取支出结构分析")
async def get_expense_structure(
    period_start: date = Query(..., description="周期开始日期"),
    period_end: date = Query(..., description="周期结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取支出结构分析
    
    - 按分类统计支出
    - 计算各分类占比
    - 标注成本行为类型
    - 支持自定义时间范围
    """
    result = CashFlowService.get_expense_structure(
        db=db,
        user_id=current_user.id,
        period_start=period_start,
        period_end=period_end
    )
    
    return ExpenseStructureResponse(**result)


@router.get("/break-even", response_model=BreakEvenAnalysisResponse, summary="获取盈亏平衡分析")
async def get_break_even(
    period_start: Optional[date] = Query(None, description="周期开始日期"),
    period_end: Optional[date] = Query(None, description="周期结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取盈亏平衡分析
    
    - 计算盈亏平衡点
    - 分析固定成本和变动成本
    - 计算安全边际
    - 判断盈利状态
    """
    result = CashFlowService.calculate_break_even(db, current_user.id)
    return BreakEvenAnalysisResponse(**result)


@router.get("/monthly-report", response_model=MonthlyReportResponse, summary="获取月度健康报告")
async def get_monthly_report(
    year: int = Query(..., description="年份"),
    month: int = Query(..., ge=1, le=12, description="月份"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取月度健康报告
    
    - 汇总月度收支情况
    - 分析收入和支出结构
    - 计算盈亏平衡点
    - 评估安全指数
    - 生成优化建议
    """
    result = CashFlowService.generate_monthly_report(
        db=db,
        user_id=current_user.id,
        year=year,
        month=month
    )
    return MonthlyReportResponse(**result)


@router.get("/income-volatility", response_model=IncomeVolatilityResponse, summary="获取收入波动归因")
async def get_income_volatility(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取收入波动归因分析
    
    - 分析收入波动性
    - 识别波动趋势
    - 找出主要影响因素
    - 提供优化建议
    """
    result = CashFlowService.analyze_income_volatility(db, current_user.id)
    return IncomeVolatilityResponse(**result)


@router.get("/dashboard", response_model=DashboardResponse, summary="获取仪表盘数据")
async def get_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取仪表盘汇总数据
    
    - 安全指数
    - 当前余额和昨日变动
    - 本月收支和利润
    - 近期趋势
    - 活跃预警
    - 预测摘要
    """
    data = CashFlowService.get_dashboard_data(db, current_user.id)
    
    return DashboardResponse(
        safety_index=SafetyIndexResponse(**data['safety_index']),
        current_balance=data['current_balance'],
        yesterday_change=data['yesterday_change'],
        monthly_income=data['monthly_income'],
        monthly_expense=data['monthly_expense'],
        monthly_profit=data['monthly_profit'],
        recent_trend=data['recent_trend'],
        active_alerts=data['active_alerts'],
        forecast_summary=data['forecast_summary']
    )
