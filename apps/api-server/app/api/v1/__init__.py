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

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(permission_router)
api_router.include_router(order_categories_router)
api_router.include_router(orders_router)
api_router.include_router(transaction_categories_router)
api_router.include_router(transactions_router)
api_router.include_router(upload_router)

__all__ = ["api_router"]
