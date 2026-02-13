"""
Dot-Store V2.1 订单数据模式
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict


class OrderCreate(BaseModel):
    """
    订单创建模式
    """
    amount: Decimal = Field(..., gt=0, description="订单金额，必须大于0")
    order_type: str = Field(..., min_length=1, max_length=32, description="订单类型")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="订单标签")
    order_metadata: Optional[dict] = Field(None, description="订单元数据")


class OrderUpdate(BaseModel):
    """
    订单更新模式
    """
    amount: Optional[Decimal] = Field(None, gt=0, description="订单金额")
    order_type: Optional[str] = Field(None, min_length=1, max_length=32, description="订单类型")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="订单标签")
    order_metadata: Optional[dict] = Field(None, description="订单元数据")
    status: Optional[str] = Field(None, min_length=1, max_length=32, description="订单状态")


class OrderResponse(BaseModel):
    """
    订单响应模式
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="订单ID")
    user_id: int = Field(..., description="用户ID")
    amount: Decimal = Field(..., description="订单金额")
    order_type: str = Field(..., description="订单类型")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="订单标签")
    order_metadata: Optional[dict] = Field(None, description="订单元数据")
    status: str = Field(..., description="订单状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    created_by: int = Field(..., description="创建人ID")
    is_deleted: bool = Field(False, description="是否删除")
    deleted_at: Optional[datetime] = Field(None, description="删除时间")


class OrderListResponse(BaseModel):
    """
    订单列表响应模式
    """
    items: List[OrderResponse] = Field(..., description="订单列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class OrderCategoryCreate(BaseModel):
    """
    订单分类创建模式
    """
    name: str = Field(..., min_length=1, max_length=64, description="分类名称")
    description: Optional[str] = Field(None, max_length=256, description="分类描述")


class OrderCategoryUpdate(BaseModel):
    """
    订单分类更新模式
    """
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="分类名称")
    description: Optional[str] = Field(None, max_length=256, description="分类描述")


class OrderCategoryResponse(BaseModel):
    """
    订单分类响应模式
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="分类ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class OrderFilters(BaseModel):
    """
    订单筛选条件
    """
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    order_type: Optional[str] = Field(None, description="订单类型")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="标签筛选")
    status: Optional[str] = Field(None, description="订单状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")
