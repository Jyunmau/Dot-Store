from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.order import Order
from models.base import Base
from models.database import get_db

# 创建订单路由
router = APIRouter()

@router.post("/", response_model=dict)
def create_order(order_data: dict, db: Session = Depends(get_db)):
    """创建订单"""
    try:
        # 创建订单对象
        order = Order(
            shop_id=order_data.get("shop_id"),
            status=order_data.get("status", "recorded"),
            amount_estimate=order_data.get("amount_estimate"),
            tags=order_data.get("tags"),
            metadata_=order_data.get("metadata")
        )
        
        # 保存到数据库
        db.add(order)
        db.commit()
        db.refresh(order)
        
        return {"id": order.id, "message": "订单创建成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建订单失败: {str(e)}")

@router.get("/{order_id}", response_model=dict)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    return {
        "id": order.id,
        "shop_id": order.shop_id,
        "status": order.status,
        "amount_estimate": order.amount_estimate,
        "tags": order.tags,
        "metadata": order.metadata_,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }

@router.put("/{order_id}", response_model=dict)
def update_order(order_id: int, order_data: dict, db: Session = Depends(get_db)):
    """更新订单"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    try:
        # 更新订单字段
        if "status" in order_data:
            order.status = order_data["status"]
        if "amount_estimate" in order_data:
            order.amount_estimate = order_data["amount_estimate"]
        if "tags" in order_data:
            order.tags = order_data["tags"]
        if "metadata" in order_data:
            order.metadata_ = order_data["metadata"]
        
        db.commit()
        db.refresh(order)
        
        return {"id": order.id, "message": "订单更新成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新订单失败: {str(e)}")

@router.get("/", response_model=List[dict])
def get_orders(shop_id: int, db: Session = Depends(get_db)):
    """获取订单列表"""
    orders = db.query(Order).filter(Order.shop_id == shop_id).all()
    
    return [{
        "id": order.id,
        "shop_id": order.shop_id,
        "status": order.status,
        "amount_estimate": order.amount_estimate,
        "tags": order.tags,
        "metadata": order.metadata_,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    } for order in orders]
