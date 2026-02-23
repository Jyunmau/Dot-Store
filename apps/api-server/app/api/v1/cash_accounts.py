"""
Dot-Store V2.2 现金账户API路由
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...services import cash_account_service
from ...schemas.cash_account import (
    CashAccountResponse,
    CashAccountUpdate,
    RecordIncomeRequest,
    RecordExpenseRequest,
    CashTransactionResponse,
    CashTransactionListResponse,
    CashSummaryResponse
)

router = APIRouter(prefix="/cash", tags=["现金账户"])


@router.get("/account", response_model=CashAccountResponse, summary="获取现金账户")
def get_cash_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取现金账户
    
    - 每个用户只有一个现金账户
    - 如果不存在会自动创建
    """
    account = cash_account_service.CashAccountService.get_account(
        db=db,
        user_id=current_user.id
    )
    return account


@router.put("/account", response_model=CashAccountResponse, summary="更新现金账户信息")
def update_cash_account(
    data: CashAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    更新现金账户信息
    
    - 可更新账户名称
    """
    account = cash_account_service.CashAccountService.update_account(
        db=db,
        user_id=current_user.id,
        account_name=data.account_name,
        operator_id=current_user.id,
        ip_address=request.client.host if request else None
    )
    return account


@router.post("/income", response_model=CashTransactionResponse, summary="记录收入")
def record_income(
    data: RecordIncomeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    记录收入
    
    - 收入金额必须大于0
    - 可关联订单ID或客户交易ID
    - 收入分类：order_income(订单收入)、recharge_income(充值收入)、refund_income(退款收入)、other_income(其他收入)
    """
    try:
        transaction = cash_account_service.CashAccountService.record_income(
            db=db,
            user_id=current_user.id,
            amount=data.amount,
            category=data.category,
            order_id=data.order_id,
            customer_transaction_id=data.customer_transaction_id,
            note=data.note,
            operator_id=current_user.id,
            ip_address=request.client.host if request else None
        )
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/expense", response_model=CashTransactionResponse, summary="记录支出")
def record_expense(
    data: RecordExpenseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    记录支出
    
    - 支出金额必须大于0
    - 余额必须充足
    - 支出分类：purchase(采购支出)、salary(工资支出)、rent(房租支出)、utility(水电费)、other_expense(其他支出)
    """
    try:
        transaction = cash_account_service.CashAccountService.record_expense(
            db=db,
            user_id=current_user.id,
            amount=data.amount,
            category=data.category,
            note=data.note,
            operator_id=current_user.id,
            ip_address=request.client.host if request else None
        )
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions", response_model=CashTransactionListResponse, summary="获取现金交易记录")
def get_cash_transactions(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    transaction_type: Optional[str] = Query(None, description="交易类型"),
    category: Optional[str] = Query(None, description="收支分类"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取现金交易记录
    
    - 支持按交易类型筛选
    - 支持按收支分类筛选
    - 支持按时间范围筛选
    - 支持分页
    """
    transactions, total = cash_account_service.CashAccountService.get_transactions(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        category=category,
        page=page,
        page_size=page_size
    )
    
    return CashTransactionListResponse(
        items=transactions,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/summary", response_model=CashSummaryResponse, summary="获取收支汇总")
def get_cash_summary(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取收支汇总
    
    - 返回总收入、总支出、净收入
    - 返回按分类统计的收支数据
    - 支持按时间范围筛选
    """
    summary = cash_account_service.CashAccountService.get_summary(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    
    return CashSummaryResponse(**summary)
