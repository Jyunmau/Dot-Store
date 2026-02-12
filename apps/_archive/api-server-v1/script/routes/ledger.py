from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from kernel.models.ledger import LedgerAccount, LedgerEntry
from shared.db.database import get_db

# 创建账务路由
router = APIRouter()

@router.post("/accounts", response_model=dict)
def create_ledger_account(account_data: dict, db: Session = Depends(get_db)):
    """创建分类账"""
    try:
        # 创建分类账对象
        account = LedgerAccount(
            shop_id=account_data.get("shop_id"),
            code=account_data.get("code"),
            name=account_data.get("name"),
            type=account_data.get("type")
        )
        
        # 保存到数据库
        db.add(account)
        db.commit()
        db.refresh(account)
        
        return {"id": account.id, "message": "分类账创建成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建分类账失败: {str(e)}")

@router.get("/accounts", response_model=List[dict])
def get_ledger_accounts(shop_id: int, db: Session = Depends(get_db)):
    """获取分类账列表"""
    accounts = db.query(LedgerAccount).filter(LedgerAccount.shop_id == shop_id).all()
    
    return [{
        "id": account.id,
        "shop_id": account.shop_id,
        "code": account.code,
        "name": account.name,
        "type": account.type,
        "created_at": account.created_at
    } for account in accounts]

@router.post("/entries", response_model=dict)
def create_ledger_entry(entry_data: dict, db: Session = Depends(get_db)):
    """创建账务分录"""
    try:
        # 创建账务分录对象
        entry = LedgerEntry(
            shop_id=entry_data.get("shop_id"),
            account_id=entry_data.get("account_id"),
            order_id=entry_data.get("order_id"),
            event_id=entry_data.get("event_id"),
            amount=entry_data.get("amount"),
            direction=entry_data.get("direction"),
            description=entry_data.get("description")
        )
        
        # 保存到数据库
        db.add(entry)
        db.commit()
        db.refresh(entry)
        
        return {"id": entry.id, "message": "账务分录创建成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建账务分录失败: {str(e)}")

@router.get("/entries", response_model=List[dict])
def get_ledger_entries(shop_id: int, db: Session = Depends(get_db)):
    """获取账务分录列表"""
    entries = db.query(LedgerEntry).filter(LedgerEntry.shop_id == shop_id).all()
    
    return [{
        "id": entry.id,
        "shop_id": entry.shop_id,
        "account_id": entry.account_id,
        "order_id": entry.order_id,
        "event_id": entry.event_id,
        "amount": entry.amount,
        "direction": entry.direction,
        "description": entry.description,
        "created_at": entry.created_at
    } for entry in entries]