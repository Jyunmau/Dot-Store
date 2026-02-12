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
from .order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
    OrderCategoryCreate,
    OrderCategoryUpdate,
    OrderCategoryResponse,
    OrderFilters,
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
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderListResponse",
    "OrderCategoryCreate",
    "OrderCategoryUpdate",
    "OrderCategoryResponse",
    "OrderFilters",
]
