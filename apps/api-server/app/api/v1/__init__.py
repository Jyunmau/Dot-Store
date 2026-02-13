"""
Dot-Store V2.1 API v1模块
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .permission import router as permission_router
from .order_categories import router as order_categories_router
from .orders import router as orders_router
from .transaction_categories import router as transaction_categories_router
from .transactions import router as transactions_router
from .upload import router as upload_router
from .reports import router as reports_router
from .stock import router as stock_router
from .backup import router as backup_router, settings_router as backup_settings_router
from .member import router as member_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(permission_router)
api_router.include_router(order_categories_router)
api_router.include_router(orders_router)
api_router.include_router(transaction_categories_router)
api_router.include_router(transactions_router)
api_router.include_router(upload_router)
api_router.include_router(reports_router)
api_router.include_router(stock_router)
api_router.include_router(backup_router)
api_router.include_router(backup_settings_router)
api_router.include_router(member_router)

__all__ = ["api_router"]
