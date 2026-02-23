"""
Dot-Store V2.2 订单API路由
"""
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderDetailResponse,
    OrderListResponse,
    OrderFilters,
    OrderVoidRequest,
    OrderSummary,
    OrderItemCreate,
    OrderItemResponse,
)
from app.services.order_service_v2 import OrderServiceV2
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
    - 支持同时创建订单项
    """
    items = None
    if order_data.items:
        items = [item.model_dump() for item in order_data.items]
    
    order = OrderServiceV2.create_order(
        db=db,
        user_id=current_user.id,
        order_type=order_data.order_type,
        amount=order_data.amount,
        payment_method=order_data.payment_method,
        customer_account_id=order_data.customer_account_id,
        category_id=order_data.category_id,
        tags=order_data.tags,
        note=order_data.note,
        items=items,
        created_by=current_user.id
    )
    return OrderResponse.model_validate(order)


@router.get("", response_model=OrderListResponse, summary="获取订单列表")
async def list_orders(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    order_type: Optional[str] = Query(None, description="订单类型"),
    status: Optional[str] = Query(None, description="订单状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单列表接口
    
    - 支持按日期范围筛选
    - 支持按订单类型筛选
    - 支持按状态筛选
    - 支持分页
    """
    orders, total = OrderServiceV2.get_orders(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        order_type=order_type,
        status=status,
        page=page,
        page_size=page_size
    )
    
    return OrderListResponse(
        items=[OrderResponse.model_validate(o) for o in orders],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/today/summary", response_model=OrderSummary, summary="获取今日汇总")
async def get_today_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取今日订单汇总
    """
    summary = OrderServiceV2.get_today_summary(db, current_user.id)
    return OrderSummary(**summary)


@router.get("/{order_id}", response_model=OrderDetailResponse, summary="获取订单详情")
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单详情接口（含订单项）
    """
    order = OrderServiceV2.get_order_with_items(db, current_user.id, order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    response = OrderDetailResponse.model_validate(order)
    if hasattr(order, 'items'):
        response.items = [OrderItemResponse.model_validate(item) for item in order.items]
    
    return response


@router.put("/{order_id}", response_model=OrderResponse, summary="更新订单")
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新订单接口
    
    - 支持更新金额、类型、支付方式、备注、状态
    """
    try:
        order = OrderServiceV2.update_order(
            db=db,
            user_id=current_user.id,
            order_id=order_id,
            **order_data.model_dump(exclude_unset=True)
        )
        return OrderResponse.model_validate(order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{order_id}/void", response_model=OrderResponse, summary="作废订单")
async def void_order(
    order_id: int,
    void_data: OrderVoidRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    作废订单接口
    
    - 订单状态变为voided
    - 记录作废原因
    - 记录事件日志
    """
    try:
        order = OrderServiceV2.void_order(
            db=db,
            user_id=current_user.id,
            order_id=order_id,
            reason=void_data.reason,
            voided_by=current_user.id
        )
        return OrderResponse.model_validate(order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{order_id}/items", response_model=list[OrderItemResponse], summary="获取订单项列表")
async def get_order_items(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取订单项列表
    """
    order = OrderServiceV2.get_order(db, current_user.id, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    items = OrderServiceV2.get_order_items(db, order_id)
    return [OrderItemResponse.model_validate(item) for item in items]


@router.post("/{order_id}/items", response_model=OrderItemResponse, summary="添加订单项")
async def add_order_item(
    order_id: int,
    item_data: OrderItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    添加订单项
    
    - 如果关联了食材ID，自动触发库存出库
    """
    try:
        from decimal import Decimal
        item = OrderServiceV2.add_order_item(
            db=db,
            user_id=current_user.id,
            order_id=order_id,
            product_name=item_data.product_name,
            quantity=Decimal(str(item_data.quantity)),
            unit_price=Decimal(str(item_data.unit_price)),
            cost_price=Decimal(str(item_data.cost_price)) if item_data.cost_price else None,
            ingredient_id=item_data.ingredient_id,
            note=item_data.note
        )
        return OrderItemResponse.model_validate(item)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{order_id}/items/{item_id}", summary="删除订单项")
async def delete_order_item(
    order_id: int,
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除订单项
    """
    try:
        OrderServiceV2.delete_order_item(db, current_user.id, item_id)
        return {"message": "订单项删除成功"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
