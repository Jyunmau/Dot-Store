"""
Dot-Store V2.1 收支分类API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.transaction import (
    TransactionCategoryCreate,
    TransactionCategoryUpdate,
    TransactionCategoryResponse,
)
from app.services.transaction_category_service import TransactionCategoryService
from app.models.user import User

router = APIRouter(prefix="/transactions/categories", tags=["收支分类管理"])


@router.post("", response_model=TransactionCategoryResponse, summary="创建收支分类")
async def create_category(
    category_data: TransactionCategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    创建收支分类接口
    
    - 类型必须为 income 或 expense
    - 分类名称为必填项
    """
    category_service = TransactionCategoryService(db)
    
    existing_category = category_service.get_category_by_name(
        current_user.id, category_data.name, category_data.type
    )
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该分类名称已存在"
        )
    
    category = category_service.create_category(current_user.id, category_data)
    return TransactionCategoryResponse.model_validate(category)


@router.get("", summary="获取收支分类列表")
async def list_categories(
    type: Optional[str] = Query(None, description="类型筛选(income/expense)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取收支分类列表接口
    
    - 支持按类型筛选（income/expense）
    """
    category_service = TransactionCategoryService(db)
    categories = category_service.list_categories(current_user.id, type)
    return [TransactionCategoryResponse.model_validate(c) for c in categories]


@router.get("/{category_id}", response_model=TransactionCategoryResponse, summary="获取收支分类详情")
async def get_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    获取收支分类详情接口
    """
    category_service = TransactionCategoryService(db)
    category = category_service.get_category(category_id, current_user.id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在"
        )

    return TransactionCategoryResponse.model_validate(category)


@router.put("/{category_id}", response_model=TransactionCategoryResponse, summary="更新收支分类")
async def update_category(
    category_id: int,
    category_data: TransactionCategoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    更新收支分类接口
    
    - 支持更新分类名称和描述
    """
    category_service = TransactionCategoryService(db)
    category = category_service.update_category(
        category_id, current_user.id, category_data
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在"
        )

    return TransactionCategoryResponse.model_validate(category)


@router.delete("/{category_id}", summary="删除收支分类")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    删除收支分类接口
    """
    category_service = TransactionCategoryService(db)
    success = category_service.delete_category(category_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在"
        )

    return {"message": "分类删除成功"}
