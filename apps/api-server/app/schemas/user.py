"""
Dot-Store V2.1 用户数据模式
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re


class UserBase(BaseModel):
    """
    用户基础模式
    """
    phone: Optional[str] = Field(None, max_length=32, description="手机号")
    email: Optional[str] = Field(None, max_length=128, description="邮箱")
    shop_name: str = Field(..., max_length=128, description="店铺名称")
    shop_type: str = Field(..., max_length=32, description="店铺类型")
    city: str = Field(..., max_length=64, description="所在城市")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            if not re.match(r'^1[3-9]\d{9}$', v):
                raise ValueError('手机号格式不正确')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
                raise ValueError('邮箱格式不正确')
        return v


class UserCreate(UserBase):
    """
    用户创建模式
    """
    password: str = Field(..., min_length=8, max_length=128, description="密码")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$', v):
            raise ValueError('密码至少8位，需包含字母和数字')
        return v

    @field_validator('phone', 'email')
    @classmethod
    def validate_contact(cls, v, info):
        if info.field_name == 'phone' and v is None:
            phone_val = info.data.get('phone')
            email_val = info.data.get('email')
            if phone_val is None and email_val is None:
                raise ValueError('手机号和邮箱至少填写一个')
        return v


class UserLogin(BaseModel):
    """
    用户登录模式
    """
    username: str = Field(..., description="手机号或邮箱")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """
    用户更新模式
    """
    phone: Optional[str] = Field(None, max_length=32)
    email: Optional[str] = Field(None, max_length=128)
    shop_name: Optional[str] = Field(None, max_length=128)
    shop_type: Optional[str] = Field(None, max_length=32)
    city: Optional[str] = Field(None, max_length=64)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            if not re.match(r'^1[3-9]\d{9}$', v):
                raise ValueError('手机号格式不正确')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
                raise ValueError('邮箱格式不正确')
        return v


class UserResponse(BaseModel):
    """
    用户响应模式
    """
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    shop_name: str
    shop_type: str
    city: str
    role: str
    status: str
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    令牌响应模式
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class StaffCreate(BaseModel):
    """
    店员创建模式
    """
    phone: Optional[str] = Field(None, max_length=32, description="手机号")
    email: Optional[str] = Field(None, max_length=128, description="邮箱")
    password: str = Field(..., min_length=8, max_length=128, description="密码")
    shop_name: Optional[str] = Field(None, max_length=128, description="店铺名称")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            if not re.match(r'^1[3-9]\d{9}$', v):
                raise ValueError('手机号格式不正确')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
                raise ValueError('邮箱格式不正确')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$', v):
            raise ValueError('密码至少8位，需包含字母和数字')
        return v


class StaffUpdate(BaseModel):
    """
    店员更新模式
    """
    phone: Optional[str] = Field(None, max_length=32)
    email: Optional[str] = Field(None, max_length=128)


class PermissionUpdate(BaseModel):
    """
    权限更新模式
    """
    permissions: List[str] = Field(..., description="权限列表")


class StaffResponse(BaseModel):
    """
    店员响应模式
    """
    id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    shop_name: str
    role: str
    status: str
    permissions: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True
