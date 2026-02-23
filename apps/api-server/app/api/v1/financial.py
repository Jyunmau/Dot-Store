"""
Dot-Store V2.2 财务快照API路由
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.financial_snapshot import (
    FinancialSnapshotCreate,
    FinancialSnapshotResponse,
    FinancialSnapshotListResponse,
    FinancialSnapshotCompare,
    FinancialTrendResponse,
    FinancialTrendItem,
)
from app.services.financial_snapshot_service import FinancialSnapshotService
from app.models.user import User

router = APIRouter(prefix="/financial", tags=["财务管理"])


@router.get("/snapshots", response_model=FinancialSnapshotListResponse, summary="获取财务快照列表")
async def get_snapshots(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    snapshot_type: Optional[str] = Query(None, description="快照类型"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取财务快照列表
    
    - 支持按日期范围筛选
    - 支持按快照类型筛选
    - 支持分页
    """
    snapshots, total = FinancialSnapshotService.get_snapshots(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        snapshot_type=snapshot_type,
        page=page,
        page_size=page_size
    )
    
    return FinancialSnapshotListResponse(
        items=[FinancialSnapshotResponse.model_validate(s) for s in snapshots],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/snapshots/today", response_model=FinancialSnapshotResponse, summary="获取或创建今日快照")
async def get_or_create_today_snapshot(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取或创建今日财务快照
    """
    snapshot = FinancialSnapshotService.get_or_create_today_snapshot(db, current_user.id)
    return FinancialSnapshotResponse.model_validate(snapshot)


@router.get("/snapshots/{snapshot_date}", response_model=FinancialSnapshotResponse, summary="获取指定日期快照")
async def get_snapshot_by_date(
    snapshot_date: date,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取指定日期的财务快照
    """
    snapshot = FinancialSnapshotService.get_snapshot(db, current_user.id, snapshot_date)
    
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该日期不存在快照"
        )
    
    return FinancialSnapshotResponse.model_validate(snapshot)


@router.post("/snapshots/{snapshot_date}", response_model=FinancialSnapshotResponse, summary="手动生成快照")
async def create_snapshot(
    snapshot_date: date,
    snapshot_type: str = Query('daily', description="快照类型"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    手动生成财务快照
    
    - 收集现金余额
    - 收集库存价值
    - 收集预收款
    - 计算当日收支
    - 执行数据校验
    - 触发事件日志
    """
    try:
        snapshot = FinancialSnapshotService.create_snapshot(
            db=db,
            user_id=current_user.id,
            snapshot_date=snapshot_date,
            snapshot_type=snapshot_type,
            operator_id=current_user.id
        )
        return FinancialSnapshotResponse.model_validate(snapshot)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/compare", response_model=FinancialSnapshotCompare, summary="对比快照")
async def compare_snapshots(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    对比两个日期的财务快照
    
    - 现金余额变化
    - 库存价值变化
    - 预收款变化
    - 净资产变化
    - 收支汇总
    """
    result = FinancialSnapshotService.compare_snapshots(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    
    if result.get('start_snapshot'):
        result['start_snapshot'] = FinancialSnapshotResponse.model_validate(result['start_snapshot'])
    if result.get('end_snapshot'):
        result['end_snapshot'] = FinancialSnapshotResponse.model_validate(result['end_snapshot'])
    
    return FinancialSnapshotCompare(**result)


@router.get("/trends", response_model=FinancialTrendResponse, summary="获取财务趋势")
async def get_trends(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取财务趋势数据
    
    - 现金余额趋势
    - 库存价值趋势
    - 预收款趋势
    - 净资产趋势
    - 收支趋势
    """
    trends = FinancialSnapshotService.get_trends(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    
    return FinancialTrendResponse(
        items=[FinancialTrendItem(**t) for t in trends],
        start_date=start_date,
        end_date=end_date
    )
