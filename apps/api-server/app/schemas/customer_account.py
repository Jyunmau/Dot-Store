"""
Dot-Store V2.2 客户账户数据模式
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator
import re


class CustomerAccountCreate(BaseModel):
    """客户账户创建模式"""
    customer_name: str = Field(..., min_length=1, max_length=64, description="客户名称")
    phone: str = Field(..., min_length=1, max_length=32, description="客户手机号")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式错误')
        return v


class CustomerAccountUpdate(BaseModel):
    """客户账户更新模式"""
    customer_name: Optional[str] = Field(None, min_length=1, max_length=64, description="客户名称")
    status: Optional[str] = Field(None, description="账户状态")


class CustomerAccountResponse(BaseModel):
    """客户账户响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="账户ID")
    user_id: int = Field(..., description="用户ID")
    customer_name: str = Field(..., description="客户名称")
    phone: str = Field(..., description="客户手机号")
    balance: Decimal = Field(..., description="当前余额")
    total_recharged: Decimal = Field(..., description="累计充值金额")
    total_consumed: Decimal = Field(..., description="累计消费金额")
    status: str = Field(..., description="账户状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class CustomerAccountListResponse(BaseModel):
    """客户账户列表响应模式"""
    items: List[CustomerAccountResponse] = Field(..., description="账户列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class RechargeRequest(BaseModel):
    """充值请求模式"""
    amount: Decimal = Field(..., gt=0, description="充值金额，必须大于0")
    note: Optional[str] = Field(None, description="备注")


class ConsumeRequest(BaseModel):
    """消费请求模式"""
    amount: Decimal = Field(..., gt=0, description="消费金额，必须大于0")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    note: Optional[str] = Field(None, description="备注")


class CustomerTransactionResponse(BaseModel):
    """客户交易响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="交易ID")
    user_id: int = Field(..., description="用户ID")
    account_id: int = Field(..., description="账户ID")
    transaction_no: str = Field(..., description="交易编号")
    transaction_type: str = Field(..., description="交易类型")
    amount: Decimal = Field(..., description="交易金额")
    balance_before: Decimal = Field(..., description="交易前余额")
    balance_after: Decimal = Field(..., description="交易后余额")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    note: Optional[str] = Field(None, description="备注")
    operator_id: int = Field(..., description="操作人ID")
    created_at: datetime = Field(..., description="创建时间")


class CustomerTransactionListResponse(BaseModel):
    """客户交易列表响应模式"""
    items: List[CustomerTransactionResponse] = Field(..., description="交易列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class RebuildBalanceResponse(BaseModel):
    """重建余额响应模式"""
    account_id: int = Field(..., description="账户ID")
    original_balance: Decimal = Field(..., description="原余额")
    calculated_balance: Decimal = Field(..., description="计算余额")
    is_consistent: bool = Field(..., description="是否一致")
