"""
Dot-Store V2.2 认证服务
"""
from datetime import datetime, timedelta
from typing import Optional
import json
import secrets
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, StaffCreate
from ..core.config import settings
from ..core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)


class AuthService:
    """
    认证服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """
        根据手机号获取用户
        """
        return self.db.query(User).filter(User.phone == phone).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名（手机号或邮箱）获取用户
        """
        return self.db.query(User).filter(
            or_(User.phone == username, User.email == username)
        ).first()

    def register(self, user_data: UserCreate) -> User:
        """
        用户注册
        """
        if not user_data.phone and not user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号和邮箱至少填写一个"
            )

        if user_data.phone:
            existing_user = self.get_user_by_phone(user_data.phone)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该手机号已被注册"
                )

        if user_data.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该邮箱已被注册"
                )

        user = User(
            phone=user_data.phone,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            shop_name=user_data.shop_name,
            shop_type=user_data.shop_type,
            city=user_data.city,
            role="owner",
            status="active",
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def login(self, login_data: UserLogin) -> dict:
        """
        用户登录
        """
        user = self.get_user_by_username(login_data.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )

        if user.is_locked():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"账户已被锁定，请{settings.LOCKOUT_DURATION_MINUTES}分钟后重试"
            )

        if not verify_password(login_data.password, user.password_hash):
            user.login_attempts += 1
            if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user.locked_until = datetime.utcnow() + timedelta(
                    minutes=settings.LOCKOUT_DURATION_MINUTES
                )
            self.db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )

        if user.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被禁用"
            )

        user.login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.utcnow()
        self.db.commit()

        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }

    def logout(self, user_id: int) -> bool:
        """
        用户登出
        """
        return True

    def refresh_token(self, refresh_token: str) -> dict:
        """
        刷新令牌
        """
        from ..core.security import decode_token

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )

        user_id = payload.get("sub")
        user = self.get_user_by_id(user_id)

        if not user or user.status != "active":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )

        new_access_token = create_access_token(data={"sub": user.id})
        new_refresh_token = create_refresh_token(data={"sub": user.id})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    def create_staff(self, owner_id: int, staff_data: StaffCreate) -> User:
        """
        创建店员
        """
        owner = self.get_user_by_id(owner_id)
        if not owner or owner.role != "owner":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有店主可以添加店员"
            )

        if not staff_data.phone and not staff_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号和邮箱至少填写一个"
            )

        if staff_data.phone:
            existing_user = self.get_user_by_phone(staff_data.phone)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该手机号已被注册"
                )

        if staff_data.email:
            existing_user = self.get_user_by_email(staff_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该邮箱已被注册"
                )

        user = User(
            phone=staff_data.phone,
            email=staff_data.email,
            password_hash=get_password_hash(staff_data.password),
            shop_name=staff_data.shop_name or owner.shop_name,
            shop_type=owner.shop_type,
            city=owner.city,
            role="staff",
            status="active",
            permissions=json.dumps([]),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_staff_list(self, owner_id: int) -> list[User]:
        """
        获取店员列表
        """
        owner = self.get_user_by_id(owner_id)
        if not owner or owner.role != "owner":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有店主可以查看店员列表"
            )

        return self.db.query(User).filter(
            User.shop_name == owner.shop_name,
            User.role == "staff"
        ).all()

    def get_staff_by_id(self, staff_id: int, owner_id: int) -> Optional[User]:
        """
        获取店员详情
        """
        owner = self.get_user_by_id(owner_id)
        if not owner or owner.role != "owner":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有店主可以查看店员详情"
            )

        staff = self.get_user_by_id(staff_id)
        if not staff or staff.role != "staff" or staff.shop_name != owner.shop_name:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="店员不存在"
            )

        return staff

    def update_staff_permissions(self, staff_id: int, owner_id: int, permissions: list[str]) -> User:
        """
        更新店员权限
        """
        staff = self.get_staff_by_id(staff_id, owner_id)
        staff.permissions = json.dumps(permissions)
        self.db.commit()
        self.db.refresh(staff)
        return staff

    def remove_staff(self, staff_id: int, owner_id: int) -> bool:
        """
        移除店员
        """
        staff = self.get_staff_by_id(staff_id, owner_id)
        self.db.delete(staff)
        self.db.commit()
        return True

    def update_user(self, user_id: int, update_data: dict) -> User:
        """
        更新用户信息
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def generate_api_key(self, user_id: int, expires_days: Optional[int] = None) -> dict:
        """
        生成API密钥
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        if user.role != "owner":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有店主可以生成API密钥"
            )

        api_key = f"sk_{secrets.token_hex(16)}"
        now = datetime.utcnow()
        expires_at = None
        if expires_days:
            expires_at = now + timedelta(days=expires_days)

        user.api_key = api_key
        user.api_key_created_at = now
        user.api_key_expires_at = expires_at

        self.db.commit()
        self.db.refresh(user)

        return {
            "api_key": api_key,
            "created_at": now,
            "expires_at": expires_at
        }

    def revoke_api_key(self, user_id: int) -> bool:
        """
        撤销API密钥
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        user.api_key = None
        user.api_key_created_at = None
        user.api_key_expires_at = None

        self.db.commit()
        return True

    def get_api_key_status(self, user_id: int) -> dict:
        """
        获取API密钥状态
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        has_api_key = user.api_key is not None
        is_expired = False
        if has_api_key and user.api_key_expires_at:
            is_expired = datetime.utcnow() > user.api_key_expires_at

        return {
            "has_api_key": has_api_key,
            "created_at": user.api_key_created_at,
            "expires_at": user.api_key_expires_at,
            "is_expired": is_expired
        }

    def verify_api_key(self, api_key: str) -> Optional[User]:
        """
        验证API密钥
        """
        if not api_key or not api_key.startswith("sk_"):
            return None

        user = self.db.query(User).filter(User.api_key == api_key).first()
        if not user:
            return None

        if user.status != "active":
            return None

        if user.api_key_expires_at and datetime.utcnow() > user.api_key_expires_at:
            return None

        return user
