"""
Dot-Store V2.1 备份API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.backup import Backup, BackupSettings
from app.schemas.backup import (
    BackupCreate,
    BackupResponse,
    BackupListResponse,
    BackupSettingsResponse,
    BackupSettingsUpdate,
)
from app.services.backup_service import BackupService

router = APIRouter(prefix="/backups", tags=["备份管理"])


@router.post("", response_model=dict, summary="创建备份")
async def create_backup(
    backup_data: BackupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建手动备份
    
    - **name**: 备份名称
    - **description**: 备份描述（可选）
    """
    service = BackupService(db)
    backup = service.create_backup(current_user.id, backup_data)
    
    return {
        "code": 200,
        "message": "备份创建成功",
        "data": BackupResponse.model_validate(backup)
    }


@router.get("", response_model=dict, summary="获取备份列表")
async def get_backups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取备份列表
    
    - **skip**: 跳过记录数
    - **limit**: 返回记录数
    """
    service = BackupService(db)
    backups = service.get_backups(current_user.id, skip, limit)
    
    return {
        "code": 200,
        "message": "获取成功",
        "data": [BackupListResponse.model_validate(b) for b in backups]
    }


@router.get("/{backup_id}", response_model=dict, summary="获取备份详情")
async def get_backup(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取备份详情
    
    - **backup_id**: 备份ID
    """
    service = BackupService(db)
    backup = service.get_backup(current_user.id, backup_id)
    
    return {
        "code": 200,
        "message": "获取成功",
        "data": BackupResponse.model_validate(backup)
    }


@router.delete("/{backup_id}", response_model=dict, summary="删除备份")
async def delete_backup(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除备份
    
    - **backup_id**: 备份ID
    """
    service = BackupService(db)
    service.delete_backup(current_user.id, backup_id)
    
    return {
        "code": 200,
        "message": "备份删除成功",
        "data": None
    }


@router.get("/{backup_id}/download", summary="下载备份文件")
async def download_backup(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    下载备份文件
    
    - **backup_id**: 备份ID
    """
    service = BackupService(db)
    return service.download_backup(current_user.id, backup_id)


@router.post("/{backup_id}/restore", response_model=dict, summary="恢复备份")
async def restore_backup(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    从备份恢复数据
    
    注意：恢复操作将覆盖当前所有数据，请谨慎操作
    
    - **backup_id**: 备份ID
    """
    service = BackupService(db)
    result = service.restore_backup(current_user.id, backup_id)
    
    return {
        "code": 200,
        "message": "备份恢复成功",
        "data": result
    }


settings_router = APIRouter(prefix="/backup-settings", tags=["备份设置"])


@settings_router.get("", response_model=dict, summary="获取备份设置")
async def get_backup_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取备份设置
    """
    service = BackupService(db)
    settings = service.get_backup_settings(current_user.id)
    
    return {
        "code": 200,
        "message": "获取成功",
        "data": BackupSettingsResponse.model_validate(settings)
    }


@settings_router.put("", response_model=dict, summary="更新备份设置")
async def update_backup_settings(
    settings_data: BackupSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新备份设置
    
    - **auto_backup_enabled**: 是否启用自动备份
    - **backup_schedule**: 备份计划（Cron表达式）
    - **backup_retention_days**: 备份保留天数
    """
    service = BackupService(db)
    settings = service.update_backup_settings(current_user.id, settings_data)
    
    return {
        "code": 200,
        "message": "备份设置更新成功",
        "data": BackupSettingsResponse.model_validate(settings)
    }
