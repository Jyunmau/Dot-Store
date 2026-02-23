"""
Dot-Store V2.2 风险预警Schema
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class RiskAlertResponse(BaseModel):
    """风险预警响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    alert_date: date
    alert_level: str = Field(..., description="预警等级: low/medium/high/critical")
    alert_type: str = Field(..., description="预警类型")
    message: str = Field(..., description="预警信息")
    suggestions: Optional[List[str]] = None
    is_read: bool
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime


class RiskAlertListResponse(BaseModel):
    """风险预警列表响应"""
    items: List[RiskAlertResponse]
    total: int
    unread_count: int


class RiskAlertStatsResponse(BaseModel):
    """风险预警统计响应"""
    total_alerts: int = Field(..., description="总预警数")
    unread_count: int = Field(..., description="未读预警数")
    resolved_count: int = Field(..., description="已解决预警数")
    
    by_level: Dict[str, int] = Field(..., description="按等级统计")
    by_type: Dict[str, int] = Field(..., description="按类型统计")
    
    recent_alerts: List[RiskAlertResponse] = Field(..., description="最近预警")


class RiskAlertCreate(BaseModel):
    """创建风险预警"""
    alert_level: str = Field(..., description="预警等级")
    alert_type: str = Field(..., description="预警类型")
    message: str = Field(..., description="预警信息")
    suggestions: Optional[List[str]] = None


class RiskAlertResolve(BaseModel):
    """解决风险预警"""
    resolution_note: Optional[str] = Field(None, description="解决备注")
