"""
Dot-Store V2.2 现金账户数据模式
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class CashAccountResponse(BaseModel):
    """现金账户响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="账户ID")
    user_id: int = Field(..., description="用户ID")
    account_name: str = Field(..., description="账户名称")
    account_type: str = Field(..., description="账户类型")
    balance: Decimal = Field(..., description="当前余额")
    total_income: Decimal = Field(..., description="累计收入")
    total_expense: Decimal = Field(..., description="累计支出")
    status: str = Field(..., description="账户状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class CashAccountUpdate(BaseModel):
    """现金账户更新模式"""
    account_name: Optional[str] = Field(None, min_length=1, max_length=64, description="账户名称")


class RecordIncomeRequest(BaseModel):
    """记录收入请求模式"""
    amount: Decimal = Field(..., gt=0, description="收入金额，必须大于0")
    category: str = Field(..., min_length=1, max_length=64, description="收入分类")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    customer_transaction_id: Optional[int] = Field(None, description="关联客户交易ID")
    note: Optional[str] = Field(None, description="备注")


class RecordExpenseRequest(BaseModel):
    """记录支出请求模式"""
    amount: Decimal = Field(..., gt=0, description="支出金额，必须大于0")
    category: str = Field(..., min_length=1, max_length=64, description="支出分类")
    note: Optional[str] = Field(None, description="备注")


class CashTransactionResponse(BaseModel):
    """现金交易响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="交易ID")
    user_id: int = Field(..., description="用户ID")
    account_id: int = Field(..., description="账户ID")
    transaction_no: str = Field(..., description="交易编号")
    transaction_type: str = Field(..., description="交易类型")
    category: str = Field(..., description="收支分类")
    amount: Decimal = Field(..., description="交易金额")
    balance_before: Decimal = Field(..., description="交易前余额")
    balance_after: Decimal = Field(..., description="交易后余额")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    customer_transaction_id: Optional[int] = Field(None, description="关联客户交易ID")
    note: Optional[str] = Field(None, description="备注")
    operator_id: int = Field(..., description="操作人ID")
    created_at: datetime = Field(..., description="创建时间")


class CashTransactionListResponse(BaseModel):
    """现金交易列表响应模式"""
    items: List[CashTransactionResponse] = Field(..., description="交易列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class CashSummaryResponse(BaseModel):
    """现金收支汇总响应模式"""
    total_income: Decimal = Field(..., description="总收入")
    total_expense: Decimal = Field(..., description="总支出")
    net_income: Decimal = Field(..., description="净收入")
    categories: Dict[str, Decimal] = Field(default_factory=dict, description="分类统计")


class CashTransactionFilters(BaseModel):
    """现金交易筛选条件"""
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    transaction_type: Optional[str] = Field(None, description="交易类型")
    category: Optional[str] = Field(None, description="收支分类")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
