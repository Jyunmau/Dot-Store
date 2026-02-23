"""
Dot-Store V2.2 成本记录数据模式
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ExpenseRecordBase(BaseModel):
    """成本记录基础模式"""
    category: str = Field(..., description="成本分类")
    amount: float = Field(..., gt=0, description="成本金额")
    description: Optional[str] = Field(None, description="描述")
    expense_date: date = Field(..., description="成本日期")
    cost_behavior: Optional[str] = Field(None, description="成本行为")
    cost_function: Optional[str] = Field(None, description="成本功能")


class ExpenseRecordCreate(ExpenseRecordBase):
    """创建成本记录模式"""
    pass


class ExpenseRecordUpdate(BaseModel):
    """更新成本记录模式"""
    category: Optional[str] = Field(None, description="成本分类")
    amount: Optional[float] = Field(None, gt=0, description="成本金额")
    description: Optional[str] = Field(None, description="描述")
    expense_date: Optional[date] = Field(None, description="成本日期")
    cost_behavior: Optional[str] = Field(None, description="成本行为")
    cost_function: Optional[str] = Field(None, description="成本功能")


class ExpenseRecordResponse(ExpenseRecordBase):
    """成本记录响应模式"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="记录ID")
    user_id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class ExpenseRecordListResponse(BaseModel):
    """成本记录列表响应"""
    items: List[ExpenseRecordResponse] = Field(..., description="记录列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class ExpenseSummary(BaseModel):
    """成本汇总"""
    total_amount: float = Field(0, description="总金额")
    category_breakdown: Dict[str, Any] = Field(default_factory=dict, description="分类明细")
    behavior_breakdown: Dict[str, Any] = Field(default_factory=dict, description="成本行为明细")
    function_breakdown: Dict[str, Any] = Field(default_factory=dict, description="成本功能明细")


class ExpenseCategoryOption(BaseModel):
    """成本分类选项"""
    value: str = Field(..., description="分类值")
    label: str = Field(..., description="分类标签")


class ExpenseCategoryListResponse(BaseModel):
    """成本分类列表响应"""
    categories: List[ExpenseCategoryOption] = Field(..., description="分类列表")
    cost_behaviors: List[ExpenseCategoryOption] = Field(..., description="成本行为列表")
    cost_functions: List[ExpenseCategoryOption] = Field(..., description="成本功能列表")
