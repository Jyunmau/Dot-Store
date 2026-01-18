from fastapi import APIRouter

# 导入各个模块的路由
from .order import router as order_router
from .ledger import router as ledger_router
from .report import router as report_router
from .config import router as config_router
from .resource_event import router as resource_event_router

# 创建主路由
api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
api_router.include_router(ledger_router, prefix="/ledger", tags=["ledger"])
api_router.include_router(report_router, prefix="/reports", tags=["reports"])
api_router.include_router(config_router, prefix="/config", tags=["config"])
api_router.include_router(resource_event_router, prefix="/resource-events", tags=["resource-events"])
