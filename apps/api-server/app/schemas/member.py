"""
Dot-Store V2.1 会员数据模式
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class MemberCreate(BaseModel):
    """
    会员创建模式
    """
    name: str = Field(..., min_length=1, max_length=64, description="会员姓名")
    phone: str = Field(..., min_length=1, max_length=32, description="手机号")
    level: str = Field("normal", min_length=1, max_length=32, description="会员等级: normal, vip")


class MemberUpdate(BaseModel):
    """
    会员更新模式
    """
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="会员姓名")
    phone: Optional[str] = Field(None, min_length=1, max_length=32, description="手机号")
    level: Optional[str] = Field(None, min_length=1, max_length=32, description="会员等级")


class MemberResponse(BaseModel):
    """
    会员响应模式
    """
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="会员ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="会员姓名")
    phone: str = Field(..., description="手机号")
    level: str = Field(..., description="会员等级")
    points: int = Field(..., description="积分")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class MemberListResponse(BaseModel):
    """
    会员列表响应模式
    """
    items: List[MemberResponse] = Field(..., description="会员列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class PointsAddParams(BaseModel):
    """
    增加积分参数
    """
    member_id: int = Field(..., description="会员ID")
    points: int = Field(..., gt=0, description="积分数量，必须大于0")
    reason: str = Field(..., min_length=1, max_length=256, description="原因")


class PointsSubtractParams(BaseModel):
    """
    减少积分参数
    """
    member_id: int = Field(..., description="会员ID")
    points: int = Field(..., gt=0, description="积分数量，必须大于0")
    reason: str = Field(..., min_length=1, max_length=256, description="原因")


class PointsRecordResponse(BaseModel):
    """
    积分记录响应模式
    """
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="记录ID")
    member_id: int = Field(..., description="会员ID")
    user_id: int = Field(..., description="用户ID")
    type: str = Field(..., description="类型: add, subtract")
    points: int = Field(..., description="积分数量")
    reason: str = Field(..., description="原因")
    created_at: datetime = Field(..., description="创建时间")
    member_name: Optional[str] = Field(None, description="会员姓名")


class PointsRecordListResponse(BaseModel):
    """
    积分记录列表响应模式
    """
    items: List[PointsRecordResponse] = Field(..., description="积分记录列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class PointsExchangeParams(BaseModel):
    """
    积分兑换参数
    """
    member_id: int = Field(..., description="会员ID")
    points: int = Field(..., gt=0, description="兑换积分数量，必须大于0")
    amount: Decimal = Field(..., gt=0, description="兑换金额，必须大于0")


class PointsExchangeResponse(BaseModel):
    """
    积分兑换响应模式
    """
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="兑换ID")
    member_id: int = Field(..., description="会员ID")
    user_id: int = Field(..., description="用户ID")
    points: int = Field(..., description="兑换积分")
    amount: Decimal = Field(..., description="兑换金额")
    created_at: datetime = Field(..., description="创建时间")
    member_name: Optional[str] = Field(None, description="会员姓名")


class PointsExchangeListResponse(BaseModel):
    """
    积分兑换列表响应模式
    """
    items: List[PointsExchangeResponse] = Field(..., description="积分兑换列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")
