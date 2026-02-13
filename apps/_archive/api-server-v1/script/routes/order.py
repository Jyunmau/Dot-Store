from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from platforms.models.order import Order
from kernel.models.ledger import LedgerEntry, LedgerAccount
from shared.db.database import get_db

# 创建订单路由
router = APIRouter()

def get_or_create_default_account(db: Session, shop_id: int, account_type: str) -> int:
    """获取或创建默认账户"""
    # 根据类型设置账户名称和代码
    if account_type == "income":
        code = "DEFAULT_INCOME"
        name = "默认收入账户"
        acc_type = "收入账"
    else:
        code = "DEFAULT_EXPENSE"
        name = "默认成本账户"
        acc_type = "成本账"
    
    # 查找现有账户
    account = db.query(LedgerAccount).filter(
        LedgerAccount.shop_id == shop_id,
        LedgerAccount.code == code
    ).first()
    
    if not account:
        # 创建默认账户
        account = LedgerAccount(
            shop_id=shop_id,
            code=code,
            name=name,
            type=acc_type
        )
        db.add(account)
        db.commit()
        db.refresh(account)
    
    return account.id

@router.post("/", response_model=dict)
def create_order(order_data: dict, db: Session = Depends(get_db)):
    """创建订单并同步创建账务分录"""
    try:
        # 从order_data中获取必填字段
        shop_id = order_data.get("shop_id", 1) # 默认使用 shop_id=1
        
        # 获取金额字段，兼容前端传递的amount和后端使用的amount_estimate
        # 注意：前端传递的是元，后端需要转换为分存储
        amount = order_data.get("amount")
        amount_estimate = order_data.get("amount_estimate")
        
        # 确定最终金额，优先使用amount字段
        final_amount_fen = 0
        if amount is not None:
            final_amount_fen = int(round(float(amount) * 100))
        elif amount_estimate is not None:
            final_amount_fen = int(round(float(amount_estimate) * 100))
        
        # 获取tags判断是收入还是支出
        tags = order_data.get("tags", [])
        # 只要tags里包含"支出"或者type是"expense"，就认为是支出
        order_type = order_data.get("type", "order")
        is_expense = "支出" in tags or order_type == "expense"
        
        # 创建订单对象
        order = Order(
            shop_id=shop_id,
            status=order_data.get("status", "recorded"),
            amount_estimate=final_amount_fen,
            tags=tags,
            metadata_=order_data.get("metadata", {})
        )
        
        # 保存订单到数据库
        db.add(order)
        db.flush() # 先刷新获取 ID
        
        # 同步创建账务分录（LedgerEntry）以支持报表功能
        if final_amount_fen > 0:
            # 获取或创建默认账户
            account_type = "expense" if is_expense else "income"
            account_id = get_or_create_default_account(db, shop_id, account_type)
            
            # 创建账务分录
            ledger_entry = LedgerEntry(
                shop_id=shop_id,
                account_id=account_id,
                order_id=order.id,
                amount=final_amount_fen / 100.0,  # 转换回元存储
                direction="OUT" if is_expense else "IN",
                transaction_type=order_type,
                description=order_data.get("metadata", {}).get("note", "")
            )
            db.add(ledger_entry)
            db.flush() # 刷新获取分录 ID
            
            # 更新订单的ledger_entry_id
            order.ledger_entry_id = ledger_entry.id
        
        db.commit()
        db.refresh(order)
        
        # 返回创建的订单信息，包括金额
        return {
            "id": order.id, 
            "message": "订单创建成功",
            "amount_estimate": final_amount_fen / 100.0
        }
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
        "amount_estimate": (order.amount_estimate or 0) / 100.0,  # 处理null值并转换为元返回
        "tags": order.tags or [],
        "metadata": order.metadata_ or {},
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
        # 兼容amount和amount_estimate字段，并转换为整数分
        if "amount_estimate" in order_data:
            order.amount_estimate = int(float(order_data["amount_estimate"]) * 100)  # 转换为分
        elif "amount" in order_data:
            order.amount_estimate = int(float(order_data["amount"]) * 100)  # 转换为分
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
        "amount_estimate": (order.amount_estimate or 0) / 100.0,  # 处理null值并转换为元返回
        "tags": order.tags or [],
        "metadata": order.metadata_ or {},
        "created_at": order.created_at,
        "updated_at": order.updated_at
    } for order in orders]

@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """删除订单及其关联的账务分录"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    try:
        # 删除关联的账务分录
        if order.ledger_entry_id:
            ledger_entry = db.query(LedgerEntry).filter(LedgerEntry.id == order.ledger_entry_id).first()
            if ledger_entry:
                db.delete(ledger_entry)
        
        # 删除订单本身
        db.delete(order)
        db.commit()
        
        return {"id": order_id, "message": "订单删除成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除订单失败: {str(e)}")