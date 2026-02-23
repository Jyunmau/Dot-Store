"""
Dot-Store V2.2 客户账户API路由
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...services import customer_account_service
from ...schemas.customer_account import (
    CustomerAccountCreate,
    CustomerAccountUpdate,
    CustomerAccountResponse,
    CustomerAccountListResponse,
    RechargeRequest,
    ConsumeRequest,
    CustomerTransactionResponse,
    CustomerTransactionListResponse,
    RebuildBalanceResponse
)

router = APIRouter(prefix="/customers", tags=["客户账户"])


@router.post("", response_model=CustomerAccountResponse, summary="创建客户账户")
def create_customer_account(
    data: CustomerAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    创建客户账户
    
    - 每个手机号只能创建一个账户
    - 账户创建后余额为0
    """
    try:
        account = customer_account_service.CustomerAccountService.create_account(
            db=db,
            user_id=current_user.id,
            customer_name=data.customer_name,
            phone=data.phone,
            operator_id=current_user.id,
            ip_address=request.client.host if request else None
        )
        return account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=CustomerAccountListResponse, summary="获取客户账户列表")
def list_customer_accounts(
    search: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="账户状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取客户账户列表
    
    - 支持按客户名称或手机号搜索
    - 支持按状态筛选
    - 支持分页
    """
    accounts, total = customer_account_service.CustomerAccountService.list_accounts(
        db=db,
        user_id=current_user.id,
        search=search,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return CustomerAccountListResponse(
        items=accounts,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/phone/{phone}", response_model=CustomerAccountResponse, summary="按手机号查询客户账户")
def get_customer_account_by_phone(
    phone: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    按手机号查询客户账户
    """
    account = customer_account_service.CustomerAccountService.get_account_by_phone(
        db=db,
        user_id=current_user.id,
        phone=phone
    )
    
    if not account:
        raise HTTPException(status_code=404, detail="客户账户不存在")
    
    return account


@router.get("/{account_id}", response_model=CustomerAccountResponse, summary="获取客户账户详情")
def get_customer_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取客户账户详情
    """
    account = customer_account_service.CustomerAccountService.get_account(
        db=db,
        user_id=current_user.id,
        account_id=account_id
    )
    
    if not account:
        raise HTTPException(status_code=404, detail="客户账户不存在")
    
    return account


@router.put("/{account_id}", response_model=CustomerAccountResponse, summary="更新客户账户信息")
def update_customer_account(
    account_id: int,
    data: CustomerAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    更新客户账户信息
    
    - 可更新客户名称和账户状态
    """
    try:
        account = customer_account_service.CustomerAccountService.update_account(
            db=db,
            user_id=current_user.id,
            account_id=account_id,
            customer_name=data.customer_name,
            status=data.status,
            operator_id=current_user.id,
            ip_address=request.client.host if request else None
        )
        return account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{account_id}/recharge", response_model=CustomerTransactionResponse, summary="客户充值")
def recharge_customer_account(
    account_id: int,
    data: RechargeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    客户充值
    
    - 充值金额必须大于0
    - 充值后余额增加
    - 生成交易记录
    """
    try:
        transaction = customer_account_service.CustomerAccountService.recharge(
            db=db,
            user_id=current_user.id,
            account_id=account_id,
            amount=data.amount,
            note=data.note,
            operator_id=current_user.id,
            ip_address=request.client.host if request else None
        )
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{account_id}/consume", response_model=CustomerTransactionResponse, summary="客户消费")
def consume_customer_account(
    account_id: int,
    data: ConsumeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    request: Request = None
):
    """
    客户消费
    
    - 消费金额必须大于0
    - 余额必须充足
    - 可关联订单ID
    """
    try:
        transaction = customer_account_service.CustomerAccountService.consume(
            db=db,
            user_id=current_user.id,
            account_id=account_id,
            amount=data.amount,
            order_id=data.order_id,
            note=data.note,
            operator_id=current_user.id,
            ip_address=request.client.host if request else None
        )
        return transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{account_id}/transactions", response_model=CustomerTransactionListResponse, summary="获取客户交易记录")
def get_customer_transactions(
    account_id: int,
    transaction_type: Optional[str] = Query(None, description="交易类型"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取客户交易记录
    
    - 支持按交易类型筛选
    - 支持按时间范围筛选
    - 支持分页
    """
    transactions, total = customer_account_service.CustomerAccountService.get_transactions(
        db=db,
        user_id=current_user.id,
        account_id=account_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )
    
    return CustomerTransactionListResponse(
        items=transactions,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/{account_id}/rebuild-balance", response_model=RebuildBalanceResponse, summary="重建客户余额")
def rebuild_customer_balance(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    从交易记录重建余额
    
    - 用于数据校验和修复
    - 如果余额不一致，会自动修复
    """
    try:
        original, calculated, is_consistent = customer_account_service.CustomerAccountService.rebuild_balance(
            db=db,
            user_id=current_user.id,
            account_id=account_id
        )
        
        return RebuildBalanceResponse(
            account_id=account_id,
            original_balance=original,
            calculated_balance=calculated,
            is_consistent=is_consistent
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
