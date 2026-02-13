"""
Dot-Store V2.1 报表API路由
"""
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.services.report_service import ReportService
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["报表管理"])


class CustomReportRequest(BaseModel):
    """
    自定义报表请求模型
    """
    start_date: str
    end_date: str
    type: str = "all"
    categories: Optional[List[str]] = None


class ExportRequest(BaseModel):
    """
    导出报表请求模型
    """
    report_data: dict
    report_type: str


@router.get("/daily", summary="获取每日报表")
async def get_daily_report(
    date_param: Optional[str] = Query(None, alias="date", description="报表日期(YYYY-MM-DD)，默认为今天"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取每日报表接口
    
    - 显示今日订单数量、收入、支出、利润
    - 显示各分类收入和支出明细
    - 如不指定日期，默认返回今日报表
    """
    report_service = ReportService(db)
    
    parsed_date = None
    if date_param:
        try:
            parsed_date = date.fromisoformat(date_param)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="日期格式不正确，请使用YYYY-MM-DD格式"
            )
    
    report = report_service.get_daily_report(current_user.id, parsed_date)
    return {"code": 200, "message": "获取成功", "data": report}


@router.get("/weekly", summary="获取每周报表")
async def get_weekly_report(
    start_date: Optional[str] = Query(None, description="开始日期(YYYY-MM-DD)，默认为本周一"),
    end_date: Optional[str] = Query(None, description="结束日期(YYYY-MM-DD)，默认为本周日"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取每周报表接口
    
    - 显示本周订单数量、收入、支出、利润
    - 显示每日收入和支出趋势
    - 显示各分类收入和支出明细
    """
    report_service = ReportService(db)
    
    parsed_start = None
    parsed_end = None
    
    if start_date:
        try:
            parsed_start = date.fromisoformat(start_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="开始日期格式不正确，请使用YYYY-MM-DD格式"
            )
    
    if end_date:
        try:
            parsed_end = date.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期格式不正确，请使用YYYY-MM-DD格式"
            )
    
    report = report_service.get_weekly_report(current_user.id, parsed_start, parsed_end)
    return {"code": 200, "message": "获取成功", "data": report}


@router.get("/monthly", summary="获取每月报表")
async def get_monthly_report(
    year: Optional[int] = Query(None, description="年份，默认为当前年"),
    month: Optional[int] = Query(None, description="月份(1-12)，默认为当前月"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取每月报表接口
    
    - 显示本月订单数量、收入、支出、利润
    - 显示每周收入和支出趋势
    - 显示各分类收入和支出明细
    """
    report_service = ReportService(db)
    report = report_service.get_monthly_report(current_user.id, year, month)
    return {"code": 200, "message": "获取成功", "data": report}


@router.post("/custom", summary="获取自定义报表")
async def get_custom_report(
    request: CustomReportRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取自定义报表接口
    
    - 支持自定义日期范围
    - 支持按类型筛选（income/expense/all）
    - 支持按分类筛选
    """
    report_service = ReportService(db)
    
    try:
        start_date = date.fromisoformat(request.start_date)
        end_date = date.fromisoformat(request.end_date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="日期格式不正确，请使用YYYY-MM-DD格式"
        )
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="开始日期不能晚于结束日期"
        )
    
    report = report_service.get_custom_report(
        current_user.id,
        start_date,
        end_date,
        request.type,
        request.categories
    )
    return {"code": 200, "message": "获取成功", "data": report}


@router.get("/category-analysis", summary="获取分类分析")
async def get_category_analysis(
    start_date: str = Query(..., description="开始日期(YYYY-MM-DD)"),
    end_date: str = Query(..., description="结束日期(YYYY-MM-DD)"),
    type: str = Query("all", description="类型(income/expense/all)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取分类分析接口
    
    - 按分类统计收入和支出
    - 支持按类型筛选
    - 返回各分类金额和占比
    """
    report_service = ReportService(db)
    
    try:
        parsed_start = date.fromisoformat(start_date)
        parsed_end = date.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="日期格式不正确，请使用YYYY-MM-DD格式"
        )
    
    analysis = report_service.get_category_analysis(
        current_user.id,
        parsed_start,
        parsed_end,
        type
    )
    return {"code": 200, "message": "获取成功", "data": analysis}


@router.post("/export/excel", summary="导出报表为Excel")
async def export_report_excel(
    request: ExportRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    导出报表为Excel格式接口
    
    - 支持日报、周报、月报、自定义报表导出
    - 返回Excel文件下载
    """
    report_service = ReportService(db)
    
    try:
        excel_file = report_service.export_report_excel(
            request.report_data,
            request.report_type
        )
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    report_type_names = {
        "daily": "每日报表",
        "weekly": "每周报表",
        "monthly": "每月报表",
        "custom": "自定义报表"
    }
    
    filename = f"{report_type_names.get(request.report_type, '报表')}.xlsx"
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/export/pdf", summary="导出报表为PDF")
async def export_report_pdf(
    request: ExportRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    导出报表为PDF格式接口
    
    - 支持日报、周报、月报、自定义报表导出
    - 返回PDF文件下载
    """
    report_service = ReportService(db)
    
    try:
        pdf_file = report_service.export_report_pdf(
            request.report_data,
            request.report_type
        )
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    report_type_names = {
        "daily": "每日报表",
        "weekly": "每周报表",
        "monthly": "每月报表",
        "custom": "自定义报表"
    }
    
    filename = f"{report_type_names.get(request.report_type, '报表')}.pdf"
    
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
