"""
Dot-Store V2.1 备份Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BackupCreate(BaseModel):
    """
    创建备份请求
    """
    name: str = Field(..., min_length=1, max_length=64, description="备份名称")
    description: Optional[str] = Field(None, max_length=500, description="备份描述")


class BackupResponse(BaseModel):
    """
    备份响应
    """
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    status: str
    backup_path: str
    backup_size: int
    backup_type: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BackupListResponse(BaseModel):
    """
    备份列表响应
    """
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    status: str
    backup_size: int
    backup_type: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BackupSettingsResponse(BaseModel):
    """
    备份设置响应
    """
    id: int
    user_id: int
    auto_backup_enabled: bool
    backup_schedule: str
    backup_retention_days: int
    last_auto_backup_at: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class BackupSettingsUpdate(BaseModel):
    """
    更新备份设置请求
    """
    auto_backup_enabled: bool = Field(..., description="是否启用自动备份")
    backup_schedule: str = Field(..., max_length=128, description="备份计划（Cron表达式）")
    backup_retention_days: int = Field(..., ge=1, le=365, description="备份保留天数")
