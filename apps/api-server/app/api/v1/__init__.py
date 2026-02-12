"""
Dot-Store V2.1 API v1模块
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .permission import router as permission_router
from .order_categories import router as order_categories_router
from .orders import router as orders_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(permission_router)
api_router.include_router(order_categories_router)
api_router.include_router(orders_router)

__all__ = ["api_router"]
