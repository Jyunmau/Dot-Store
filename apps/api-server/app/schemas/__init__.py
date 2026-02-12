"""
Dot-Store V2.1 数据模式
"""
from .user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    TokenResponse,
    StaffCreate,
    StaffUpdate,
    PermissionUpdate,
    StaffResponse,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "TokenResponse",
    "StaffCreate",
    "StaffUpdate",
    "PermissionUpdate",
    "StaffResponse",
]
