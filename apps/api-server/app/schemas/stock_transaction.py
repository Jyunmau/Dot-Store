"""
Dot-Store V2.2 库存流水数据模式
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class StockTransactionType:
    """库存交易类型枚举"""
    PURCHASE = 'purchase'
    CONSUME = 'consume'
    ADJUST_ADD = 'adjust_add'
    ADJUST_SUB = 'adjust_sub'
    RETURN = 'return'
    TRANSFER_IN = 'transfer_in'
    TRANSFER_OUT = 'transfer_out'


class StockInRequest(BaseModel):
    """入库请求"""
    ingredient_id: int = Field(..., description="食材ID")
    quantity: Decimal = Field(..., gt=0, description="入库数量")
    cost: Optional[Decimal] = Field(None, ge=0, description="成本单价")
    note: Optional[str] = Field(None, description="备注")


class StockOutRequest(BaseModel):
    """出库请求"""
    ingredient_id: int = Field(..., description="食材ID")
    quantity: Decimal = Field(..., gt=0, description="出库数量")
    note: Optional[str] = Field(None, description="备注")


class StockAdjustRequest(BaseModel):
    """库存调整请求"""
    ingredient_id: int = Field(..., description="食材ID")
    quantity: Decimal = Field(..., description="调整数量（正数增加，负数减少）")
    note: Optional[str] = Field(None, description="备注")


class StockTransactionResponse(BaseModel):
    """库存流水响应"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="流水ID")
    user_id: int = Field(..., description="用户ID")
    ingredient_id: int = Field(..., description="食材ID")
    transaction_no: str = Field(..., description="交易编号")
    transaction_type: str = Field(..., description="交易类型")
    quantity: Decimal = Field(..., description="变动数量")
    stock_before: Decimal = Field(..., description="变动前库存")
    stock_after: Decimal = Field(..., description="变动后库存")
    unit_cost: Optional[Decimal] = Field(None, description="单位成本")
    total_cost: Optional[Decimal] = Field(None, description="总成本")
    note: Optional[str] = Field(None, description="备注")
    operator_id: int = Field(..., description="操作人ID")
    created_at: datetime = Field(..., description="创建时间")


class StockTransactionListResponse(BaseModel):
    """库存流水列表响应"""
    items: List[StockTransactionResponse] = Field(..., description="流水列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class StockWarning(BaseModel):
    """库存预警"""
    ingredient_id: int = Field(..., description="食材ID")
    ingredient_name: str = Field(..., description="食材名称")
    current_stock: float = Field(..., description="当前库存")
    min_stock: Optional[float] = Field(None, description="最低库存")
    expiry_date: Optional[str] = Field(None, description="过期日期")
    unit: str = Field(..., description="单位")
    warning_type: str = Field(..., description="预警类型")
    message: str = Field(..., description="预警消息")


class StockSummary(BaseModel):
    """库存汇总"""
    total_ingredients: int = Field(0, description="食材总数")
    total_value: float = Field(0, description="库存总价值")
    low_stock_count: int = Field(0, description="低库存数量")
    expiring_count: int = Field(0, description="即将过期数量")


class IngredientCreate(BaseModel):
    """食材创建模式"""
    name: str = Field(..., min_length=1, max_length=64, description="食材名称")
    unit: str = Field(..., min_length=1, max_length=16, description="计量单位")
    current_stock: Decimal = Field(0, ge=0, description="当前库存")
    min_stock: Decimal = Field(0, ge=0, description="最低库存")
    cost_per_unit: Decimal = Field(0, ge=0, description="成本单价")
    category: Optional[str] = Field(None, max_length=64, description="分类")
    supplier: Optional[str] = Field(None, max_length=128, description="供应商")
    expiry_date: Optional[date] = Field(None, description="过期日期")


class IngredientUpdate(BaseModel):
    """食材更新模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="食材名称")
    unit: Optional[str] = Field(None, min_length=1, max_length=16, description="计量单位")
    current_stock: Optional[Decimal] = Field(None, ge=0, description="当前库存")
    min_stock: Optional[Decimal] = Field(None, ge=0, description="最低库存")
    cost_per_unit: Optional[Decimal] = Field(None, ge=0, description="成本单价")
    category: Optional[str] = Field(None, max_length=64, description="分类")
    supplier: Optional[str] = Field(None, max_length=128, description="供应商")
    expiry_date: Optional[date] = Field(None, description="过期日期")
    status: Optional[str] = Field(None, description="状态")


class IngredientResponse(BaseModel):
    """食材响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="食材ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="食材名称")
    unit: str = Field(..., description="计量单位")
    current_stock: Decimal = Field(..., description="当前库存")
    min_stock: Decimal = Field(0, description="最低库存")
    cost_per_unit: Decimal = Field(0, description="成本单价")
    warning_stock: Decimal = Field(0, description="预警库存")
    category: Optional[str] = Field(None, description="分类")
    supplier: Optional[str] = Field(None, description="供应商")
    expiry_date: Optional[date] = Field(None, description="过期日期")
    status: str = Field('active', description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class IngredientListResponse(BaseModel):
    """食材列表响应"""
    items: List[IngredientResponse] = Field(..., description="食材列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")
