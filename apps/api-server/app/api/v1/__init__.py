"""
Dot-Store V2.1 API v1模块
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .permission import router as permission_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(permission_router)

__all__ = ["api_router"]
