"""
Dot-Store V2.1 权限服务
"""
from typing import List, Optional
import json
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.user import User
from ..core.security import get_current_user


class PermissionService:
    """
    权限服务类
    """

    DEFAULT_OWNER_PERMISSIONS = [
        "order:create", "order:read", "order:update", "order:delete",
        "transaction:create", "transaction:read", "transaction:update", "transaction:delete",
        "report:read", "report:export",
        "stock:create", "stock:read", "stock:update", "stock:delete",
        "member:create", "member:read", "member:update", "member:delete",
        "backup:create", "backup:read", "backup:restore",
        "staff:create", "staff:read", "staff:update", "staff:delete",
    ]

    DEFAULT_STAFF_PERMISSIONS = [
        "order:create", "order:read", "order:update",
        "transaction:create", "transaction:read",
        "report:read",
    ]

    def __init__(self, db: Session):
        self.db = db

    def get_user_permissions(self, user: User) -> List[str]:
        """
        获取用户权限列表
        """
        if user.role == "owner":
            return self.DEFAULT_OWNER_PERMISSIONS

        if user.permissions:
            try:
                return json.loads(user.permissions)
            except json.JSONDecodeError:
                return self.DEFAULT_STAFF_PERMISSIONS

        return self.DEFAULT_STAFF_PERMISSIONS

    def check_permission(self, user: User, required_permission: str) -> bool:
        """
        检查用户是否有指定权限
        """
        if user.role == "owner":
            return True

        permissions = self.get_user_permissions(user)
        return required_permission in permissions

    def has_any_permission(self, user: User, required_permissions: List[str]) -> bool:
        """
        检查用户是否有任一权限
        """
        if user.role == "owner":
            return True

        permissions = self.get_user_permissions(user)
        return any(perm in permissions for perm in required_permissions)

    def has_all_permissions(self, user: User, required_permissions: List[str]) -> bool:
        """
        检查用户是否有所有权限
        """
        if user.role == "owner":
            return True

        permissions = self.get_user_permissions(user)
        return all(perm in permissions for perm in required_permissions)

    def validate_permissions(self, permissions: List[str]) -> List[str]:
        """
        验证权限列表是否有效
        """
        valid_permissions = set(self.DEFAULT_OWNER_PERMISSIONS)
        invalid_permissions = [p for p in permissions if p not in valid_permissions]
        
        if invalid_permissions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的权限: {', '.join(invalid_permissions)}"
            )
        
        return permissions

    def get_permission_groups(self) -> dict:
        """
        获取权限分组
        """
        return {
            "order": {
                "name": "订单管理",
                "permissions": [
                    {"key": "order:create", "name": "创建订单"},
                    {"key": "order:read", "name": "查看订单"},
                    {"key": "order:update", "name": "编辑订单"},
                    {"key": "order:delete", "name": "删除订单"},
                ]
            },
            "transaction": {
                "name": "收支管理",
                "permissions": [
                    {"key": "transaction:create", "name": "创建收支"},
                    {"key": "transaction:read", "name": "查看收支"},
                    {"key": "transaction:update", "name": "编辑收支"},
                    {"key": "transaction:delete", "name": "删除收支"},
                ]
            },
            "report": {
                "name": "报表管理",
                "permissions": [
                    {"key": "report:read", "name": "查看报表"},
                    {"key": "report:export", "name": "导出报表"},
                ]
            },
            "stock": {
                "name": "库存管理",
                "permissions": [
                    {"key": "stock:create", "name": "创建库存"},
                    {"key": "stock:read", "name": "查看库存"},
                    {"key": "stock:update", "name": "编辑库存"},
                    {"key": "stock:delete", "name": "删除库存"},
                ]
            },
            "member": {
                "name": "会员管理",
                "permissions": [
                    {"key": "member:create", "name": "创建会员"},
                    {"key": "member:read", "name": "查看会员"},
                    {"key": "member:update", "name": "编辑会员"},
                    {"key": "member:delete", "name": "删除会员"},
                ]
            },
            "backup": {
                "name": "数据备份",
                "permissions": [
                    {"key": "backup:create", "name": "创建备份"},
                    {"key": "backup:read", "name": "查看备份"},
                    {"key": "backup:restore", "name": "恢复备份"},
                ]
            },
            "staff": {
                "name": "店员管理",
                "permissions": [
                    {"key": "staff:create", "name": "添加店员"},
                    {"key": "staff:read", "name": "查看店员"},
                    {"key": "staff:update", "name": "编辑店员"},
                    {"key": "staff:delete", "name": "删除店员"},
                ]
            },
        }


def require_permission(permission: str):
    """
    权限装饰器
    """
    async def decorator(user = None):
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="未登录"
            )
        return user
    return decorator
