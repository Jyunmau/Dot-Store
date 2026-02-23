"""
Dot-Store V2.2 风险预警API路由
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.risk_alert import (
    RiskAlertResponse,
    RiskAlertListResponse,
    RiskAlertStatsResponse,
    RiskAlertResolve,
)
from app.services.risk_alert_service import RiskAlertService
from app.models.user import User

router = APIRouter(prefix="/risk-alerts", tags=["风险预警"])


@router.get("", response_model=RiskAlertListResponse, summary="获取风险预警列表")
async def get_alerts(
    include_resolved: bool = Query(False, description="是否包含已解决"),
    level: Optional[str] = Query(None, description="预警等级筛选"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取风险预警列表
    
    - 支持按等级筛选
    - 支持分页
    - 默认只显示未解决的预警
    """
    alerts, total = RiskAlertService.get_alerts(
        db=db,
        user_id=current_user.id,
        include_resolved=include_resolved,
        level=level,
        limit=limit,
        offset=offset
    )
    
    unread_count = sum(1 for a in alerts if not a.is_read)
    
    return RiskAlertListResponse(
        items=[RiskAlertResponse.model_validate(a) for a in alerts],
        total=total,
        unread_count=unread_count
    )


@router.get("/stats", response_model=RiskAlertStatsResponse, summary="获取风险预警统计")
async def get_alert_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取风险预警统计信息
    
    - 总预警数
    - 未读预警数
    - 已解决预警数
    - 按等级统计
    - 按类型统计
    - 最近预警
    """
    stats = RiskAlertService.get_alert_stats(db, current_user.id)
    
    return RiskAlertStatsResponse(
        total_alerts=stats['total_alerts'],
        unread_count=stats['unread_count'],
        resolved_count=stats['resolved_count'],
        by_level=stats['by_level'],
        by_type=stats['by_type'],
        recent_alerts=[RiskAlertResponse.model_validate(a) for a in stats['recent_alerts']]
    )


@router.post("/check", summary="手动触发风险检查")
async def check_risks(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    手动触发风险检查
    
    - 检查所有风险类型
    - 生成新的预警
    - 返回新生成的预警列表
    """
    alerts = RiskAlertService.check_all_risks(db, current_user.id)
    
    return {
        "message": f"检查完成，发现{len(alerts)}个新预警",
        "alerts": [RiskAlertResponse.model_validate(a) for a in alerts]
    }


@router.put("/{alert_id}/read", response_model=RiskAlertResponse, summary="标记预警为已读")
async def mark_as_read(
    alert_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    标记单个预警为已读
    """
    alert = RiskAlertService.mark_as_read(db, current_user.id, alert_id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="预警不存在"
        )
    
    return RiskAlertResponse.model_validate(alert)


@router.put("/read-all", summary="标记所有预警为已读")
async def mark_all_as_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    标记所有预警为已读
    """
    count = RiskAlertService.mark_all_as_read(db, current_user.id)
    
    return {
        "message": f"已标记{count}条预警为已读"
    }


@router.put("/{alert_id}/resolve", response_model=RiskAlertResponse, summary="解决预警")
async def resolve_alert(
    alert_id: int,
    request: RiskAlertResolve = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    解决预警
    
    - 标记预警为已解决
    - 记录解决时间
    - 可选添加解决备注
    """
    resolution_note = request.resolution_note if request else None
    
    alert = RiskAlertService.resolve_alert(
        db=db,
        user_id=current_user.id,
        alert_id=alert_id,
        resolution_note=resolution_note
    )
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="预警不存在"
        )
    
    return RiskAlertResponse.model_validate(alert)
