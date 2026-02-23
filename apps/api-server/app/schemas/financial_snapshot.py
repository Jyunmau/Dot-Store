"""
Dot-Store V2.2 财务快照数据模式
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class FinancialSnapshotBase(BaseModel):
    """财务快照基础模式"""
    snapshot_date: date = Field(..., description="快照日期")
    snapshot_type: str = Field('daily', description="快照类型")


class FinancialSnapshotCreate(FinancialSnapshotBase):
    """创建财务快照模式"""
    pass


class FinancialSnapshotResponse(FinancialSnapshotBase):
    """财务快照响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="快照ID")
    user_id: int = Field(..., description="用户ID")
    cash_balance: float = Field(0, description="现金余额")
    customer_prepaid: float = Field(0, description="预收权益负债")
    inventory_value: float = Field(0, description="库存价值")
    total_assets: float = Field(0, description="总资产")
    total_liabilities: float = Field(0, description="总负债")
    net_assets: float = Field(0, description="净资产")
    daily_revenue: float = Field(0, description="当日收入")
    daily_expense: float = Field(0, description="当日支出")
    daily_profit: float = Field(0, description="当日利润")
    order_count: int = Field(0, description="订单数量")
    validation_status: str = Field('pending', description="校验状态")
    validation_errors: Optional[dict] = Field(None, description="校验错误")
    created_at: datetime = Field(..., description="创建时间")


class FinancialSnapshotListResponse(BaseModel):
    """财务快照列表响应"""
    items: List[FinancialSnapshotResponse] = Field(..., description="快照列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class FinancialSnapshotCompare(BaseModel):
    """财务快照对比"""
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    start_snapshot: Optional[dict] = Field(None, description="开始快照")
    end_snapshot: Optional[dict] = Field(None, description="结束快照")
    cash_balance_change: float = Field(0, description="现金余额变化")
    inventory_value_change: float = Field(0, description="库存价值变化")
    customer_prepaid_change: float = Field(0, description="预收款变化")
    net_assets_change: float = Field(0, description="净资产变化")
    total_revenue: float = Field(0, description="总收入")
    total_expense: float = Field(0, description="总支出")
    total_profit: float = Field(0, description="总利润")


class FinancialTrendItem(BaseModel):
    """财务趋势项"""
    snapshot_date: date = Field(..., description="日期")
    cash_balance: float = Field(0, description="现金余额")
    inventory_value: float = Field(0, description="库存价值")
    customer_prepaid: float = Field(0, description="预收款")
    net_assets: float = Field(0, description="净资产")
    daily_revenue: float = Field(0, description="当日收入")
    daily_expense: float = Field(0, description="当日支出")
    daily_profit: float = Field(0, description="当日利润")
    order_count: int = Field(0, description="订单数量")


class FinancialTrendResponse(BaseModel):
    """财务趋势响应"""
    items: List[FinancialTrendItem] = Field(..., description="趋势数据")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
