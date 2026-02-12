"""
Dot-Store V2.1 权限API路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.permission_service import PermissionService
from app.models.user import User

router = APIRouter(prefix="/permission", tags=["权限"])


@router.get("/groups", summary="获取权限分组")
async def get_permission_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取权限分组列表
    """
    permission_service = PermissionService(db)
    return permission_service.get_permission_groups()


@router.get("/me", summary="获取当前用户权限")
async def get_my_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的权限列表
    """
    permission_service = PermissionService(db)
    permissions = permission_service.get_user_permissions(current_user)
    
    return {
        "role": current_user.role,
        "permissions": permissions
    }


@router.get("/check", summary="检查权限")
async def check_permission(
    permission: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    检查当前用户是否有指定权限
    """
    permission_service = PermissionService(db)
    has_permission = permission_service.check_permission(current_user, permission)
    
    return {
        "permission": permission,
        "has_permission": has_permission
    }
