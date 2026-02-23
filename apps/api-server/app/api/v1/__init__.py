"""
Dot-Store V2.2 API v1模块
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
from .push import router as push_router
from .events import router as events_router
from .stock_transactions import router as stock_transactions_router
from .customer_accounts import router as customer_accounts_router
from .cash_accounts import router as cash_accounts_router
from .expenses import router as expenses_router
from .financial import router as financial_router
from .cashflow import router as cashflow_router
from .risk_alerts import router as risk_alerts_router
from .preferences import router as preferences_router

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
api_router.include_router(push_router)
api_router.include_router(events_router)
api_router.include_router(stock_transactions_router)
api_router.include_router(customer_accounts_router)
api_router.include_router(cash_accounts_router)
api_router.include_router(expenses_router)
api_router.include_router(financial_router)
api_router.include_router(cashflow_router)
api_router.include_router(risk_alerts_router)
api_router.include_router(preferences_router)

__all__ = ["api_router"]
