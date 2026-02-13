"""
Dot-Store V2.1 收支记录API路由
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse,
    TransactionFilters,
    TransactionSummary,
)
from app.services.transaction_service import TransactionService
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["收支记录管理"])


@router.post("", response_model=TransactionResponse, summary="创建收支记录")
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    创建收支记录接口
    
    - 类型必须为 income 或 expense
    - 金额必须大于0
    - 分类为必填项
    - 可选关联订单、备注、凭证图片
    """
    transaction_service = TransactionService(db)
    transaction = transaction_service.create_transaction(
        current_user.id, transaction_data, current_user.id
    )
    return TransactionResponse.model_validate(transaction)


@router.get("", response_model=TransactionListResponse, summary="获取收支记录列表")
async def list_transactions(
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    type: Optional[str] = Query(None, description="类型筛选(income/expense)"),
    category: Optional[str] = Query(None, description="分类筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取收支记录列表接口
    
    - 支持按日期范围筛选
    - 支持按类型筛选（income/expense）
    - 支持按分类筛选
    - 支持分页
    """
    transaction_service = TransactionService(db)

    filters = TransactionFilters(
        start_date=start_date,
        end_date=end_date,
        type=type,
        category=category,
        page=page,
        page_size=page_size,
    )

    result = transaction_service.list_transactions(current_user.id, filters)

    return TransactionListResponse(
        items=[TransactionResponse.model_validate(t) for t in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/summary", response_model=TransactionSummary, summary="获取收支汇总统计")
async def get_transaction_summary(
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取收支汇总统计接口
    
    - 返回总收入、总支出、净利润
    - 返回各分类统计
    - 支持按日期范围筛选
    """
    transaction_service = TransactionService(db)
    summary = transaction_service.get_transaction_summary(
        current_user.id, start_date, end_date
    )
    return TransactionSummary(**summary)


@router.get("/categories", summary="获取收支分类名称列表")
async def get_transaction_categories(
    type: Optional[str] = Query(None, description="类型筛选(income/expense)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取用户所有收支分类名称列表
    """
    transaction_service = TransactionService(db)
    categories = transaction_service.get_categories_by_type(current_user.id, type)
    return {"categories": categories}


@router.post("/batch", summary="批量创建收支记录")
async def batch_create_transactions(
    transactions_data: List[TransactionCreate],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    批量创建收支记录接口
    
    - 支持批量创建多条收支记录
    - 返回创建的记录数量和列表
    """
    transaction_service = TransactionService(db)
    transactions = transaction_service.batch_create_transactions(
        current_user.id, transactions_data, current_user.id
    )
    return {
        "created_count": len(transactions),
        "transactions": [
            TransactionResponse.model_validate(t) for t in transactions
        ],
    }


@router.get("/{transaction_id}", response_model=TransactionResponse, summary="获取收支记录详情")
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取收支记录详情接口
    """
    transaction_service = TransactionService(db)
    transaction = transaction_service.get_transaction(transaction_id, current_user.id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="收支记录不存在"
        )

    return TransactionResponse.model_validate(transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse, summary="更新收支记录")
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    更新收支记录接口
    
    - 支持更新分类、金额、关联订单、备注、凭证图片
    """
    transaction_service = TransactionService(db)
    transaction = transaction_service.update_transaction(
        transaction_id, current_user.id, transaction_data
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="收支记录不存在"
        )

    return TransactionResponse.model_validate(transaction)


@router.delete("/{transaction_id}", summary="删除收支记录")
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    删除收支记录接口
    """
    transaction_service = TransactionService(db)
    success = transaction_service.delete_transaction(transaction_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="收支记录不存在"
        )

    return {"message": "收支记录删除成功"}
