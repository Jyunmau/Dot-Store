"""
Dot-Store V2.2 用户偏好配置Schema
"""
from datetime import time
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class UserPreferenceResponse(BaseModel):
    """用户偏好配置响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    
    weekly_reminder_enabled: bool
    weekly_reminder_day: int = Field(..., description="周几提醒(1-7, 1=周一)")
    weekly_reminder_time: str = Field(..., description="提醒时间(HH:MM)")
    
    monthly_report_enabled: bool
    monthly_report_day: int = Field(..., description="每月几号提醒(1-28)")
    monthly_report_time: str = Field(..., description="提醒时间(HH:MM)")
    
    risk_alert_enabled: bool
    risk_alert_threshold: str = Field(..., description="风险预警阈值: low/medium/high")
    
    notification_channels: List[str] = Field(..., description="通知渠道")


class UserPreferenceUpdate(BaseModel):
    """更新用户偏好配置"""
    weekly_reminder_enabled: Optional[bool] = None
    weekly_reminder_day: Optional[int] = Field(None, ge=1, le=7, description="周几提醒(1-7)")
    weekly_reminder_time: Optional[str] = Field(None, description="提醒时间(HH:MM)")
    
    monthly_report_enabled: Optional[bool] = None
    monthly_report_day: Optional[int] = Field(None, ge=1, le=28, description="每月几号提醒")
    monthly_report_time: Optional[str] = Field(None, description="提醒时间(HH:MM)")
    
    risk_alert_enabled: Optional[bool] = None
    risk_alert_threshold: Optional[str] = Field(None, description="风险预警阈值: low/medium/high")
    
    notification_channels: Optional[List[str]] = None


class UserPreferenceCreate(BaseModel):
    """创建用户偏好配置"""
    weekly_reminder_enabled: bool = True
    weekly_reminder_day: int = Field(default=1, ge=1, le=7)
    weekly_reminder_time: str = "10:00"
    
    monthly_report_enabled: bool = True
    monthly_report_day: int = Field(default=1, ge=1, le=28)
    monthly_report_time: str = "09:00"
    
    risk_alert_enabled: bool = True
    risk_alert_threshold: str = "medium"
    
    notification_channels: List[str] = Field(default=["push"])
