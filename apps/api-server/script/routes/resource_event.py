from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from ...kernel.models.event import Event
from ...kernel.models.resource import Resource
from ...shared.db.database import get_db

# 创建资源事件路由
router = APIRouter()

@router.post("/", response_model=dict)
def create_resource_event(event_data: dict = Body(...), db: Session = Depends(get_db)):
    """创建资源事件 - 在Reservation Service中使用，用于管理资源占用"""
    try:
        # 验证关联的资源是否存在
        if "related_resource_id" in event_data:
            resource = db.query(Resource).filter(
                Resource.id == event_data["related_resource_id"],
                Resource.shop_id == event_data.get("shop_id")
            ).first()
            if not resource:
                raise HTTPException(status_code=404, detail="关联的资源不存在")
        
        # 创建事件对象
        event = Event(
            shop_id=event_data.get("shop_id"),
            event_type=event_data.get("event_type"),
            related_resource_id=event_data.get("related_resource_id"),
            related_resource_type=event_data.get("related_resource_type"),
            actor_id=event_data.get("actor_id"),
            actor_type=event_data.get("actor_type"),
            payload=event_data.get("payload")
        )
        
        # 保存到数据库
        db.add(event)
        db.commit()
        db.refresh(event)
        
        return {"id": event.id, "message": "资源事件创建成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建资源事件失败: {str(e)}")

@router.get("/{event_id}", response_model=dict)
def get_resource_event(event_id: int, db: Session = Depends(get_db)):
    """获取资源事件详情"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="资源事件不存在")
    
    return {
        "id": event.id,
        "shop_id": event.shop_id,
        "event_type": event.event_type,
        "related_resource_id": event.related_resource_id,
        "related_resource_type": event.related_resource_type,
        "actor_id": event.actor_id,
        "actor_type": event.actor_type,
        "payload": event.payload,
        "created_at": event.created_at
    }

@router.get("/", response_model=List[dict])
def get_resource_events(
    shop_id: int,
    resource_id: int = None,
    resource_type: str = None,
    event_type: str = None,
    start_time: str = None,
    end_time: str = None,
    db: Session = Depends(get_db)
):
    """获取资源事件列表"""
    query = db.query(Event).filter(Event.shop_id == shop_id)
    
    # 添加过滤条件
    if resource_id:
        query = query.filter(Event.related_resource_id == resource_id)
    if resource_type:
        query = query.filter(Event.related_resource_type == resource_type)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if start_time:
        query = query.filter(Event.created_at >= start_time)
    if end_time:
        query = query.filter(Event.created_at <= end_time)
    
    events = query.order_by(Event.created_at.desc()).all()
    
    return [{
        "id": event.id,
        "shop_id": event.shop_id,
        "event_type": event.event_type,
        "related_resource_id": event.related_resource_id,
        "related_resource_type": event.related_resource_type,
        "actor_id": event.actor_id,
        "actor_type": event.actor_type,
        "payload": event.payload,
        "created_at": event.created_at
    } for event in events]

@router.delete("/{event_id}", response_model=dict)
def delete_resource_event(event_id: int, db: Session = Depends(get_db)):
    """删除资源事件（仅用于测试和特殊情况）"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="资源事件不存在")
    
    try:
        db.delete(event)
        db.commit()
        return {"message": "资源事件删除成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除资源事件失败: {str(e)}")