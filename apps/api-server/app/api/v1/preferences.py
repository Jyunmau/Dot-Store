"""
Dot-Store V2.2 用户偏好配置API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.user_preference import (
    UserPreferenceResponse,
    UserPreferenceUpdate,
)
from app.services.user_preference_service import UserPreferenceService
from app.models.user import User

router = APIRouter(prefix="/preferences", tags=["用户偏好配置"])


@router.get("", response_model=UserPreferenceResponse, summary="获取用户偏好配置")
async def get_preference(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的偏好配置
    
    - 如果不存在则自动创建默认配置
    - 包含周提醒、月度报告、风险预警等设置
    """
    preference = UserPreferenceService.get_or_create(db, current_user.id)
    return UserPreferenceResponse.model_validate(preference)


@router.put("", response_model=UserPreferenceResponse, summary="更新用户偏好配置")
async def update_preference(
    request: UserPreferenceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新用户偏好配置
    
    - 支持部分更新
    - 只更新提供的字段
    """
    update_data = request.model_dump(exclude_unset=True)
    
    preference = UserPreferenceService.update(
        db=db,
        user_id=current_user.id,
        **update_data
    )
    
    return UserPreferenceResponse.model_validate(preference)


@router.put("/weekly-reminder", response_model=UserPreferenceResponse, summary="更新周提醒设置")
async def update_weekly_reminder(
    enabled: bool = None,
    day: int = None,
    time: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新周提醒设置
    
    - enabled: 是否启用周提醒
    - day: 周几提醒(1-7, 1=周一)
    - time: 提醒时间(HH:MM)
    """
    preference = UserPreferenceService.update_weekly_reminder(
        db=db,
        user_id=current_user.id,
        enabled=enabled,
        day=day,
        time_str=time
    )
    
    return UserPreferenceResponse.model_validate(preference)


@router.put("/monthly-report", response_model=UserPreferenceResponse, summary="更新月度报告设置")
async def update_monthly_report(
    enabled: bool = None,
    day: int = None,
    time: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新月度报告设置
    
    - enabled: 是否启用月度报告
    - day: 每月几号发送(1-28)
    - time: 发送时间(HH:MM)
    """
    preference = UserPreferenceService.update_monthly_report(
        db=db,
        user_id=current_user.id,
        enabled=enabled,
        day=day,
        time_str=time
    )
    
    return UserPreferenceResponse.model_validate(preference)


@router.put("/risk-alert", response_model=UserPreferenceResponse, summary="更新风险预警设置")
async def update_risk_alert(
    enabled: bool = None,
    threshold: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新风险预警设置
    
    - enabled: 是否启用风险预警
    - threshold: 预警阈值(low/medium/high)
      - low: 所有等级预警
      - medium: 中等级及以上预警
      - high: 仅高等级预警
    """
    preference = UserPreferenceService.update_risk_alert(
        db=db,
        user_id=current_user.id,
        enabled=enabled,
        threshold=threshold
    )
    
    return UserPreferenceResponse.model_validate(preference)


@router.put("/notification-channels", response_model=UserPreferenceResponse, summary="更新通知渠道")
async def update_notification_channels(
    channels: List[str],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新通知渠道
    
    - 支持的渠道: push, email, sms
    - 至少保留一个渠道
    """
    preference = UserPreferenceService.update_notification_channels(
        db=db,
        user_id=current_user.id,
        channels=channels
    )
    
    return UserPreferenceResponse.model_validate(preference)


@router.post("/reset", response_model=UserPreferenceResponse, summary="重置为默认设置")
async def reset_preference(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    重置用户偏好配置为默认值
    
    - 周提醒: 周一 10:00
    - 月度报告: 每月1号 09:00
    - 风险预警: 中等级及以上
    - 通知渠道: 推送
    """
    preference = UserPreferenceService.reset_to_default(db, current_user.id)
    return UserPreferenceResponse.model_validate(preference)
