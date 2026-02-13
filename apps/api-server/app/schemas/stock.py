"""
Dot-Store V2.1 库存数据模式
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class IngredientCreate(BaseModel):
    """
    食材创建模式
    """
    name: str = Field(..., min_length=1, max_length=64, description="食材名称")
    unit: str = Field(..., min_length=1, max_length=16, description="单位")
    current_stock: Decimal = Field(0, ge=0, description="当前库存")
    warning_stock: Decimal = Field(0, ge=0, description="预警值")


class IngredientUpdate(BaseModel):
    """
    食材更新模式
    """
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="食材名称")
    unit: Optional[str] = Field(None, min_length=1, max_length=16, description="单位")
    current_stock: Optional[Decimal] = Field(None, ge=0, description="当前库存")
    warning_stock: Optional[Decimal] = Field(None, ge=0, description="预警值")


class IngredientResponse(BaseModel):
    """
    食材响应模式
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="食材ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="食材名称")
    unit: str = Field(..., description="单位")
    current_stock: Decimal = Field(..., description="当前库存")
    warning_stock: Decimal = Field(..., description="预警值")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class IngredientListResponse(BaseModel):
    """
    食材列表响应模式
    """
    items: List[IngredientResponse] = Field(..., description="食材列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class StockRecordCreate(BaseModel):
    """
    库存记录创建模式
    """
    ingredient_id: int = Field(..., description="食材ID")
    quantity: Decimal = Field(..., gt=0, description="数量，必须大于0")
    note: Optional[str] = Field(None, max_length=500, description="备注")


class StockRecordResponse(BaseModel):
    """
    库存记录响应模式
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="记录ID")
    ingredient_id: int = Field(..., description="食材ID")
    user_id: int = Field(..., description="用户ID")
    type: str = Field(..., description="类型：in-入库，out-出库")
    quantity: Decimal = Field(..., description="数量")
    note: Optional[str] = Field(None, description="备注")
    created_at: datetime = Field(..., description="创建时间")
    ingredient_name: Optional[str] = Field(None, description="食材名称")
    ingredient_unit: Optional[str] = Field(None, description="食材单位")


class StockRecordListResponse(BaseModel):
    """
    库存记录列表响应模式
    """
    items: List[StockRecordResponse] = Field(..., description="记录列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class StockWarningResponse(BaseModel):
    """
    库存预警响应模式
    """
    ingredient_id: int = Field(..., description="食材ID")
    name: str = Field(..., description="食材名称")
    unit: str = Field(..., description="单位")
    current_stock: Decimal = Field(..., description="当前库存")
    warning_stock: Decimal = Field(..., description="预警值")
    deficit: Decimal = Field(..., description="缺口数量")


class StockSummaryResponse(BaseModel):
    """
    库存统计响应模式
    """
    total_ingredients: int = Field(..., description="食材总数")
    low_stock_count: int = Field(..., description="库存预警数量")
    total_value: Decimal = Field(..., description="库存总价值")
