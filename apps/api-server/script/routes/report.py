from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from ...kernel.models.ledger import LedgerEntry
from ...platforms.models.order import Order
from ...shared.db.database import get_db

# 创建报表路由
router = APIRouter()

@router.get("/summary", response_model=dict)
def get_report_summary(shop_id: int, date: str = None, date_range: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    """获取报表汇总"""
    try:
        # 构建查询条件
        query = db.query(LedgerEntry)
        query = query.filter(LedgerEntry.shop_id == shop_id)
        
        # 根据日期范围进行过滤
        if date:
            # 单个日期过滤
            query = query.filter(func.date(LedgerEntry.created_at) == date)
        elif date_range and start_date and end_date:
            # 自定义日期范围过滤
            query = query.filter(func.date(LedgerEntry.created_at) >= start_date)
            query = query.filter(func.date(LedgerEntry.created_at) <= end_date)
        
        # 执行查询
        entries = query.all()
        
        # 计算汇总数据
        total_income = 0.0
        total_expense = 0.0
        
        for entry in entries:
            if entry.direction == "IN":
                total_income += float(entry.amount)
            else:
                total_expense += float(entry.amount)
        
        net_profit = total_income - total_expense
        
        return {
            "shop_id": shop_id,
            "date": date,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_profit": net_profit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报表汇总失败: {str(e)}")

@router.get("/income-structure", response_model=dict)
def get_income_structure(shop_id: int, date: str = None, date_range: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    """获取收入结构"""
    try:
        # 构建查询条件
        query = db.query(LedgerEntry.account_id, func.sum(LedgerEntry.amount))
        query = query.filter(LedgerEntry.shop_id == shop_id, LedgerEntry.direction == "IN")
        
        # 根据日期范围进行过滤
        if date:
            # 单个日期过滤
            query = query.filter(func.date(LedgerEntry.created_at) == date)
        elif date_range and start_date and end_date:
            # 自定义日期范围过滤
            query = query.filter(func.date(LedgerEntry.created_at) >= start_date)
            query = query.filter(func.date(LedgerEntry.created_at) <= end_date)
        
        # 按账户分组
        query = query.group_by(LedgerEntry.account_id)
        
        # 执行查询
        results = query.all()
        
        # 构建返回数据
        income_structure = {}
        for account_id, amount in results:
            income_structure[str(account_id)] = float(amount)
        
        return {
            "shop_id": shop_id,
            "date": date,
            "income_structure": income_structure
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取收入结构失败: {str(e)}")

@router.get("/expense-structure", response_model=dict)
def get_expense_structure(shop_id: int, date: str = None, date_range: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    """获取成本结构"""
    try:
        # 构建查询条件
        query = db.query(LedgerEntry.account_id, func.sum(LedgerEntry.amount))
        query = query.filter(LedgerEntry.shop_id == shop_id, LedgerEntry.direction == "OUT")
        
        # 根据日期范围进行过滤
        if date:
            # 单个日期过滤
            query = query.filter(func.date(LedgerEntry.created_at) == date)
        elif date_range and start_date and end_date:
            # 自定义日期范围过滤
            query = query.filter(func.date(LedgerEntry.created_at) >= start_date)
            query = query.filter(func.date(LedgerEntry.created_at) <= end_date)
        
        # 按账户分组
        query = query.group_by(LedgerEntry.account_id)
        
        # 执行查询
        results = query.all()
        
        # 构建返回数据
        expense_structure = {}
        for account_id, amount in results:
            expense_structure[str(account_id)] = float(amount)
        
        return {
            "shop_id": shop_id,
            "date": date,
            "expense_structure": expense_structure
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取成本结构失败: {str(e)}")