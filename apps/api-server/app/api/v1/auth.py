"""
Dot-Store V2.1 认证API路由
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.security import (
    get_current_user,
    get_current_active_user,
    get_current_owner,
    create_access_token,
    create_refresh_token,
)
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    StaffCreate,
    StaffResponse,
    PermissionUpdate,
)
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse, summary="用户注册")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    
    - 支持手机号或邮箱注册
    - 密码至少8位，需包含字母和数字
    - 注册成功后自动登录
    """
    auth_service = AuthService(db)
    user = auth_service.register(user_data)
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - 支持手机号或邮箱登录
    - 登录失败5次后锁定账户30分钟
    """
    auth_service = AuthService(db)
    result = auth_service.login(login_data)
    
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(result["user"])
    )


@router.post("/logout", summary="用户登出")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    用户登出接口
    """
    return {"message": "登出成功"}


@router.post("/refresh", response_model=TokenResponse, summary="刷新令牌")
async def refresh_token(
    refresh_token_data: dict,
    db: Session = Depends(get_db)
):
    """
    刷新令牌接口
    """
    auth_service = AuthService(db)
    result = auth_service.refresh_token(refresh_token_data.get("refresh_token", ""))
    
    user = auth_service.get_user_by_id(
        int(result["access_token"].split(".")[0]) if "." in result["access_token"] else 0
    )
    
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(user) if user else None
    )


@router.get("/users/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前登录用户信息
    """
    return UserResponse.model_validate(current_user)


@router.post("/staff", response_model=StaffResponse, summary="添加店员")
async def create_staff(
    staff_data: StaffCreate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """
    添加店员接口（仅店主可用）
    """
    auth_service = AuthService(db)
    staff = auth_service.create_staff(current_user.id, staff_data)
    
    return StaffResponse(
        id=staff.id,
        phone=staff.phone,
        email=staff.email,
        shop_name=staff.shop_name,
        role=staff.role,
        status=staff.status,
        permissions=json.loads(staff.permissions) if staff.permissions else [],
        created_at=staff.created_at
    )


@router.get("/staff", response_model=list[StaffResponse], summary="获取店员列表")
async def get_staff_list(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """
    获取店员列表接口（仅店主可用）
    """
    auth_service = AuthService(db)
    staff_list = auth_service.get_staff_list(current_user.id)
    
    return [
        StaffResponse(
            id=staff.id,
            phone=staff.phone,
            email=staff.email,
            shop_name=staff.shop_name,
            role=staff.role,
            status=staff.status,
            permissions=json.loads(staff.permissions) if staff.permissions else [],
            created_at=staff.created_at
        )
        for staff in staff_list
    ]


@router.get("/staff/{staff_id}", response_model=StaffResponse, summary="获取店员详情")
async def get_staff_detail(
    staff_id: int,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """
    获取店员详情接口（仅店主可用）
    """
    auth_service = AuthService(db)
    staff = auth_service.get_staff_by_id(staff_id, current_user.id)
    
    return StaffResponse(
        id=staff.id,
        phone=staff.phone,
        email=staff.email,
        shop_name=staff.shop_name,
        role=staff.role,
        status=staff.status,
        permissions=json.loads(staff.permissions) if staff.permissions else [],
        created_at=staff.created_at
    )


@router.put("/staff/{staff_id}/permissions", response_model=StaffResponse, summary="更新店员权限")
async def update_staff_permissions(
    staff_id: int,
    permission_data: PermissionUpdate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """
    更新店员权限接口（仅店主可用）
    """
    auth_service = AuthService(db)
    staff = auth_service.update_staff_permissions(
        staff_id, current_user.id, permission_data.permissions
    )
    
    return StaffResponse(
        id=staff.id,
        phone=staff.phone,
        email=staff.email,
        shop_name=staff.shop_name,
        role=staff.role,
        status=staff.status,
        permissions=json.loads(staff.permissions) if staff.permissions else [],
        created_at=staff.created_at
    )


@router.delete("/staff/{staff_id}", summary="移除店员")
async def remove_staff(
    staff_id: int,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """
    移除店员接口（仅店主可用）
    """
    auth_service = AuthService(db)
    auth_service.remove_staff(staff_id, current_user.id)
    
    return {"message": "店员移除成功"}
