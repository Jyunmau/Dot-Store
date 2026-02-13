"""
Dot-Store V2.1 订单分类API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.order import (
    OrderCategoryCreate,
    OrderCategoryUpdate,
    OrderCategoryResponse,
)
from app.services.order_category_service import OrderCategoryService
from app.models.user import User

router = APIRouter(prefix="/orders/categories", tags=["订单分类管理"])


@router.post("", response_model=OrderCategoryResponse, summary="创建订单分类")
async def create_category(
    category_data: OrderCategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建订单分类接口
    
    - 分类名称为必填项
    - 分类描述为可选项
    """
    category_service = OrderCategoryService(db)
    category = category_service.create_category(current_user.id, category_data)
    return OrderCategoryResponse.model_validate(category)


@router.get("", response_model=List[OrderCategoryResponse], summary="获取订单分类列表")
async def list_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单分类列表接口
    
    - 返回当前用户的所有订单分类
    """
    category_service = OrderCategoryService(db)
    categories = category_service.list_categories(current_user.id)
    return [OrderCategoryResponse.model_validate(cat) for cat in categories]


@router.get("/{category_id}", response_model=OrderCategoryResponse, summary="获取订单分类详情")
async def get_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单分类详情接口
    """
    category_service = OrderCategoryService(db)
    category = category_service.get_category(category_id, current_user.id)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    
    return OrderCategoryResponse.model_validate(category)


@router.put("/{category_id}", response_model=OrderCategoryResponse, summary="更新订单分类")
async def update_category(
    category_id: int,
    category_data: OrderCategoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新订单分类接口
    
    - 支持更新分类名称和描述
    """
    category_service = OrderCategoryService(db)
    category = category_service.update_category(category_id, current_user.id, category_data)
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    
    return OrderCategoryResponse.model_validate(category)


@router.delete("/{category_id}", summary="删除订单分类")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除订单分类接口
    
    - 如果分类下有订单，将返回错误
    """
    category_service = OrderCategoryService(db)
    
    usage_count = category_service.get_category_usage_count(category_id, current_user.id)
    if usage_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该分类下有{usage_count}个订单，无法删除"
        )
    
    success = category_service.delete_category(category_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    
    return {"message": "分类删除成功"}


@router.get("/{category_id}/usage", summary="获取分类使用情况")
async def get_category_usage(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取分类使用情况接口
    
    - 返回该分类下的订单数量
    """
    category_service = OrderCategoryService(db)
    
    category = category_service.get_category(category_id, current_user.id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    
    usage_count = category_service.get_category_usage_count(category_id, current_user.id)
    
    return {
        "category_id": category_id,
        "category_name": category.name,
        "order_count": usage_count
    }
