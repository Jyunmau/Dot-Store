"""
Dot-Store V2.2 事件相关Schema
"""
from enum import Enum
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel


class EventCategory(str, Enum):
    """事件分类"""
    AUTH = 'auth'
    ORDER = 'order'
    STOCK = 'stock'
    CUSTOMER = 'customer'
    CASH = 'cash'
    FINANCE = 'finance'
    SYSTEM = 'system'
    MCP = 'mcp'


class EventType(str, Enum):
    """事件类型"""
    USER_LOGIN = 'user_login'
    USER_LOGOUT = 'user_logout'
    USER_REGISTER = 'user_register'
    API_KEY_GENERATED = 'api_key_generated'
    
    ORDER_CREATED = 'order_created'
    ORDER_UPDATED = 'order_updated'
    ORDER_VOIDED = 'order_voided'
    
    STOCK_IN = 'stock_in'
    STOCK_OUT = 'stock_out'
    STOCK_ADJUST = 'stock_adjust'
    INGREDIENT_CREATED = 'ingredient_created'
    
    CUSTOMER_CREATED = 'customer_created'
    CUSTOMER_RECHARGE = 'customer_recharge'
    CUSTOMER_CONSUME = 'customer_consume'
    CUSTOMER_ACCOUNT_CREATED = 'customer_account_created'
    CUSTOMER_ACCOUNT_UPDATED = 'customer_account_updated'
    
    CASH_INCOME = 'cash_income'
    CASH_EXPENSE = 'cash_expense'
    CASH_ACCOUNT_CREATED = 'cash_account_created'
    CASH_ACCOUNT_UPDATED = 'cash_account_updated'
    
    FINANCIAL_SNAPSHOT_CREATED = 'financial_snapshot_created'
    
    BACKUP_CREATED = 'backup_created'
    BACKUP_RESTORED = 'backup_restored'
    
    MCP_TOOL_CALLED = 'mcp_tool_called'
    MCP_RESOURCE_ACCESSED = 'mcp_resource_accessed'


class BusinessEventBase(BaseModel):
    """业务事件基础Schema"""
    event_type: str
    event_category: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    data: Optional[dict] = None


class BusinessEventCreate(BusinessEventBase):
    """创建业务事件Schema"""
    pass


class BusinessEventResponse(BusinessEventBase):
    """业务事件响应Schema"""
    id: int
    user_id: int
    operator_id: int
    operator_type: str
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """事件列表响应"""
    items: List[BusinessEventResponse]
    total: int
    page: int
    page_size: int
