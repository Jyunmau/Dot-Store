"""
Dot-Store V2.2 成本记录API路由
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.expense_record import (
    ExpenseRecordCreate,
    ExpenseRecordUpdate,
    ExpenseRecordResponse,
    ExpenseRecordListResponse,
    ExpenseSummary,
    ExpenseCategoryListResponse,
)
from app.services.expense_record_service import ExpenseRecordService
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["成本管理"])


@router.get("", response_model=ExpenseRecordListResponse, summary="获取成本记录列表")
async def get_expenses(
    category: Optional[str] = Query(None, description="成本分类"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    cost_behavior: Optional[str] = Query(None, description="成本行为"),
    cost_function: Optional[str] = Query(None, description="成本功能"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取成本记录列表
    
    - 支持按分类筛选
    - 支持按日期范围筛选
    - 支持按成本行为筛选
    - 支持按成本功能筛选
    - 支持分页
    """
    expenses, total = ExpenseRecordService.get_expenses(
        db=db,
        user_id=current_user.id,
        category=category,
        start_date=start_date,
        end_date=end_date,
        cost_behavior=cost_behavior,
        cost_function=cost_function,
        page=page,
        page_size=page_size
    )
    
    return ExpenseRecordListResponse(
        items=[ExpenseRecordResponse.model_validate(e) for e in expenses],
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=ExpenseRecordResponse, summary="创建成本记录")
async def create_expense(
    expense_data: ExpenseRecordCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建成本记录
    
    - 记录成本金额
    - 记录成本分类
    - 记录成本日期
    - 触发事件日志
    """
    try:
        expense = ExpenseRecordService.create_expense(
            db=db,
            user_id=current_user.id,
            category=expense_data.category,
            amount=Decimal(str(expense_data.amount)),
            expense_date=expense_data.expense_date,
            description=expense_data.description,
            cost_behavior=expense_data.cost_behavior,
            cost_function=expense_data.cost_function,
            operator_id=current_user.id
        )
        return ExpenseRecordResponse.model_validate(expense)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/categories", response_model=ExpenseCategoryListResponse, summary="获取成本分类选项")
async def get_categories(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取成本分类选项
    
    - 成本分类列表
    - 成本行为列表
    - 成本功能列表
    """
    options = ExpenseRecordService.get_category_options()
    return ExpenseCategoryListResponse(**options)


@router.get("/summary", response_model=ExpenseSummary, summary="获取成本汇总")
async def get_summary(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取成本汇总
    
    - 总金额
    - 分类明细
    - 成本行为明细
    - 成本功能明细
    """
    summary = ExpenseRecordService.get_summary(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    return ExpenseSummary(**summary)


@router.get("/{expense_id}", response_model=ExpenseRecordResponse, summary="获取成本记录详情")
async def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取成本记录详情
    """
    expense = ExpenseRecordService.get_expense(db, current_user.id, expense_id)
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成本记录不存在"
        )
    
    return ExpenseRecordResponse.model_validate(expense)


@router.put("/{expense_id}", response_model=ExpenseRecordResponse, summary="更新成本记录")
async def update_expense(
    expense_id: int,
    expense_data: ExpenseRecordUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新成本记录
    
    - 更新成本信息
    - 触发事件日志
    """
    try:
        expense = ExpenseRecordService.update_expense(
            db=db,
            user_id=current_user.id,
            expense_id=expense_id,
            category=expense_data.category,
            amount=Decimal(str(expense_data.amount)) if expense_data.amount else None,
            description=expense_data.description,
            expense_date=expense_data.expense_date,
            cost_behavior=expense_data.cost_behavior,
            cost_function=expense_data.cost_function,
            operator_id=current_user.id
        )
        
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="成本记录不存在"
            )
        
        return ExpenseRecordResponse.model_validate(expense)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{expense_id}", summary="删除成本记录")
async def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除成本记录
    
    - 删除成本记录
    - 触发事件日志
    """
    success = ExpenseRecordService.delete_expense(
        db=db,
        user_id=current_user.id,
        expense_id=expense_id,
        operator_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成本记录不存在"
        )
    
    return {"message": "成本记录删除成功"}
