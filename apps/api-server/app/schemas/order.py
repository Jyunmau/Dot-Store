"""
Dot-Store V2.2 订单数据模式
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict


class OrderType:
    """订单类型枚举"""
    DINE_IN = 'dine_in'
    TAKE_OUT = 'take_out'
    PICKUP = 'pickup'


class PaymentMethod:
    """支付方式枚举"""
    CASH = 'cash'
    CUSTOMER_ACCOUNT = 'customer_account'
    WECHAT = 'wechat'
    ALIPAY = 'alipay'
    MIXED = 'mixed'


class OrderItemCreate(BaseModel):
    """订单项创建模式"""
    product_name: str = Field(..., min_length=1, max_length=128, description="产品名称")
    quantity: Decimal = Field(..., gt=0, description="数量")
    unit_price: Decimal = Field(..., ge=0, description="单价")
    cost_price: Optional[Decimal] = Field(None, ge=0, description="成本价")
    note: Optional[str] = Field(None, description="备注")


class OrderItemResponse(BaseModel):
    """订单项响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="订单项ID")
    order_id: int = Field(..., description="订单ID")
    product_name: str = Field(..., description="产品名称")
    quantity: Decimal = Field(..., description="数量")
    unit_price: Decimal = Field(..., description="单价")
    cost_price: Optional[Decimal] = Field(None, description="成本价")
    amount: Decimal = Field(..., description="金额")
    note: Optional[str] = Field(None, description="备注")
    created_at: datetime = Field(..., description="创建时间")


class OrderCreate(BaseModel):
    """订单创建模式"""
    order_type: str = Field(..., min_length=1, max_length=32, description="订单类型")
    amount: Decimal = Field(..., gt=0, description="订单金额，必须大于0")
    payment_method: Optional[str] = Field(None, max_length=32, description="支付方式")
    customer_account_id: Optional[int] = Field(None, description="客户账户ID")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="订单标签")
    note: Optional[str] = Field(None, description="备注")
    items: Optional[List[OrderItemCreate]] = Field(None, description="订单项列表")


class OrderUpdate(BaseModel):
    """订单更新模式"""
    amount: Optional[Decimal] = Field(None, gt=0, description="订单金额")
    order_type: Optional[str] = Field(None, min_length=1, max_length=32, description="订单类型")
    payment_method: Optional[str] = Field(None, max_length=32, description="支付方式")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="订单标签")
    note: Optional[str] = Field(None, description="备注")
    status: Optional[str] = Field(None, min_length=1, max_length=32, description="订单状态")


class OrderVoidRequest(BaseModel):
    """订单作废请求"""
    reason: str = Field(..., min_length=1, description="作废原因")


class OrderResponse(BaseModel):
    """订单响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="订单ID")
    user_id: int = Field(..., description="用户ID")
    order_no: str = Field(..., description="订单编号")
    order_type: str = Field(..., description="订单类型")
    amount: Decimal = Field(..., description="订单金额")
    payment_method: Optional[str] = Field(None, description="支付方式")
    customer_account_id: Optional[int] = Field(None, description="客户账户ID")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="订单标签")
    note: Optional[str] = Field(None, description="备注")
    status: str = Field(..., description="订单状态")
    is_deleted: bool = Field(False, description="是否删除")
    deleted_at: Optional[datetime] = Field(None, description="删除时间")
    deleted_by: Optional[int] = Field(None, description="删除人ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    created_by: int = Field(..., description="创建人ID")


class OrderDetailResponse(OrderResponse):
    """订单详情响应模式"""
    items: Optional[List[OrderItemResponse]] = Field(None, description="订单项列表")


class OrderListResponse(BaseModel):
    """订单列表响应模式"""
    items: List[OrderResponse] = Field(..., description="订单列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class OrderSummary(BaseModel):
    """订单汇总"""
    total_orders: int = Field(0, description="总订单数")
    total_amount: Decimal = Field(0, description="总金额")
    by_type: dict = Field(default_factory=dict, description="按类型统计")
    by_payment: dict = Field(default_factory=dict, description="按支付方式统计")


class OrderCategoryCreate(BaseModel):
    """订单分类创建模式"""
    name: str = Field(..., min_length=1, max_length=64, description="分类名称")
    description: Optional[str] = Field(None, max_length=256, description="分类描述")


class OrderCategoryUpdate(BaseModel):
    """订单分类更新模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="分类名称")
    description: Optional[str] = Field(None, max_length=256, description="分类描述")


class OrderCategoryResponse(BaseModel):
    """订单分类响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="分类ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class OrderFilters(BaseModel):
    """订单筛选条件"""
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    order_type: Optional[str] = Field(None, description="订单类型")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: Optional[List[str]] = Field(None, description="标签筛选")
    status: Optional[str] = Field(None, description="订单状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")
