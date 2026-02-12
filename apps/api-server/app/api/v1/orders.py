"""
Dot-Store V2.1 订单API路由
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
    OrderFilters,
)
from app.services.order_service import OrderService
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["订单管理"])


@router.post("", response_model=OrderResponse, summary="创建订单")
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建订单接口
    
    - 金额必须大于0
    - 订单类型为必填项
    - 标签和元数据为可选
    """
    order_service = OrderService(db)
    order = order_service.create_order(current_user.id, order_data, current_user.id)
    return OrderResponse.model_validate(order)


@router.get("", response_model=OrderListResponse, summary="获取订单列表")
async def list_orders(
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    order_type: Optional[str] = Query(None, description="订单类型"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    status: Optional[str] = Query(None, description="订单状态"),
    tags: Optional[str] = Query(None, description="标签筛选，逗号分隔"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单列表接口
    
    - 支持按日期范围筛选
    - 支持按订单类型筛选
    - 支持按分类筛选
    - 支持按状态筛选
    - 支持按标签筛选
    - 支持分页
    """
    order_service = OrderService(db)
    
    tags_list = tags.split(",") if tags else None
    
    filters = OrderFilters(
        start_date=start_date,
        end_date=end_date,
        order_type=order_type,
        category_id=category_id,
        status=status,
        tags=tags_list,
        page=page,
        page_size=page_size,
    )
    
    result = order_service.list_orders(current_user.id, filters)
    
    return OrderListResponse(
        items=[OrderResponse.model_validate(order) for order in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/recycle", response_model=OrderListResponse, summary="获取回收站订单")
async def get_recycle_orders(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取回收站订单列表接口
    
    - 返回已删除的订单
    - 支持分页
    """
    order_service = OrderService(db)
    result = order_service.get_deleted_orders(current_user.id, page, page_size)
    
    return OrderListResponse(
        items=[OrderResponse.model_validate(order) for order in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/types", summary="获取订单类型列表")
async def get_order_types(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取用户所有订单类型列表
    """
    order_service = OrderService(db)
    types = order_service.get_order_types(current_user.id)
    return {"types": types}


@router.get("/tags", summary="获取订单标签列表")
async def get_order_tags(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取用户所有订单标签列表
    """
    order_service = OrderService(db)
    tags = order_service.get_order_tags(current_user.id)
    return {"tags": tags}


@router.get("/{order_id}", response_model=OrderResponse, summary="获取订单详情")
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单详情接口
    """
    order_service = OrderService(db)
    order = order_service.get_order(order_id, current_user.id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    return OrderResponse.model_validate(order)


@router.put("/{order_id}", response_model=OrderResponse, summary="更新订单")
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新订单接口
    
    - 支持更新金额、类型、标签、元数据、状态
    """
    order_service = OrderService(db)
    order = order_service.update_order(order_id, current_user.id, order_data)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    return OrderResponse.model_validate(order)


@router.delete("/{order_id}", summary="删除订单")
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除订单接口（软删除）
    
    - 订单将移入回收站
    - 可通过回收站恢复
    """
    order_service = OrderService(db)
    success = order_service.delete_order(order_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    return {"message": "订单删除成功"}


@router.post("/{order_id}/restore", response_model=OrderResponse, summary="恢复订单")
async def restore_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    恢复订单接口
    
    - 从回收站恢复订单
    """
    order_service = OrderService(db)
    order = order_service.restore_order(order_id, current_user.id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在或不在回收站中"
        )
    
    return OrderResponse.model_validate(order)
