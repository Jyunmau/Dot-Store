"""
Dot-Store V2.1 收支记录数据模式
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class TransactionCreate(BaseModel):
    """
    收支记录创建模式
    """
    type: str = Field(..., pattern="^(income|expense)$", description="类型：income或expense")
    category: str = Field(..., min_length=1, max_length=64, description="分类名称")
    amount: Decimal = Field(..., gt=0, description="金额，必须大于0")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    note: Optional[str] = Field(None, max_length=500, description="备注")
    attachment_url: Optional[str] = Field(None, max_length=256, description="凭证图片URL")


class TransactionUpdate(BaseModel):
    """
    收支记录更新模式
    """
    category: Optional[str] = Field(None, min_length=1, max_length=64, description="分类名称")
    amount: Optional[Decimal] = Field(None, gt=0, description="金额")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    note: Optional[str] = Field(None, max_length=500, description="备注")
    attachment_url: Optional[str] = Field(None, max_length=256, description="凭证图片URL")


class TransactionResponse(BaseModel):
    """
    收支记录响应模式
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="收支记录ID")
    user_id: int = Field(..., description="用户ID")
    type: str = Field(..., description="类型：income或expense")
    category: str = Field(..., description="分类名称")
    amount: Decimal = Field(..., description="金额")
    order_id: Optional[int] = Field(None, description="关联订单ID")
    note: Optional[str] = Field(None, description="备注")
    attachment_url: Optional[str] = Field(None, description="凭证图片URL")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    created_by: int = Field(..., description="创建人ID")


class TransactionListResponse(BaseModel):
    """
    收支记录列表响应模式
    """
    items: List[TransactionResponse] = Field(..., description="收支记录列表")
    total: int = Field(..., description="总数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页数量")


class TransactionFilters(BaseModel):
    """
    收支记录筛选条件
    """
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    type: Optional[str] = Field(None, pattern="^(income|expense)$", description="类型筛选")
    category: Optional[str] = Field(None, description="分类筛选")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class TransactionSummary(BaseModel):
    """
    收支汇总统计模式
    """
    income: Decimal = Field(0, description="总收入")
    expense: Decimal = Field(0, description="总支出")
    net_profit: Decimal = Field(0, description="净利润")
    categories: Dict[str, Decimal] = Field(default_factory=dict, description="分类统计")


class TransactionCategoryCreate(BaseModel):
    """
    收支分类创建模式
    """
    name: str = Field(..., min_length=1, max_length=64, description="分类名称")
    type: str = Field(..., pattern="^(income|expense)$", description="分类类型：income或expense")
    description: Optional[str] = Field(None, max_length=256, description="分类描述")


class TransactionCategoryUpdate(BaseModel):
    """
    收支分类更新模式
    """
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="分类名称")
    description: Optional[str] = Field(None, max_length=256, description="分类描述")


class TransactionCategoryResponse(BaseModel):
    """
    收支分类响应模式
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="分类ID")
    user_id: int = Field(..., description="用户ID")
    name: str = Field(..., description="分类名称")
    type: str = Field(..., description="分类类型")
    description: Optional[str] = Field(None, description="分类描述")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class UploadResponse(BaseModel):
    """
    文件上传响应模式
    """
    url: str = Field(..., description="文件URL")
    filename: str = Field(..., description="文件名")
