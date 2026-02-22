"""
Dot-Store V2.2 事件日志API接口
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.business_event import BusinessEvent
from ...services.event_service import EventService
from ...schemas.event import EventListResponse, BusinessEventResponse

router = APIRouter(prefix="/events", tags=["事件日志"])


@router.get("", response_model=EventListResponse)
async def get_events(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    event_type: Optional[str] = Query(None, description="事件类型"),
    event_category: Optional[str] = Query(None, description="事件分类"),
    entity_type: Optional[str] = Query(None, description="实体类型"),
    entity_id: Optional[int] = Query(None, description="实体ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取事件列表
    """
    events, total = EventService.get_events(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        event_type=event_type,
        event_category=event_category,
        entity_type=entity_type,
        entity_id=entity_id,
        page=page,
        page_size=page_size
    )
    
    return EventListResponse(
        items=[BusinessEventResponse.model_validate(e) for e in events],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/entity/{entity_type}/{entity_id}", response_model=list)
async def get_entity_events(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取实体相关事件
    """
    events = EventService.get_entity_events(
        db=db,
        user_id=current_user.id,
        entity_type=entity_type,
        entity_id=entity_id
    )
    
    return [BusinessEventResponse.model_validate(e) for e in events]


@router.get("/{event_id}", response_model=BusinessEventResponse)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取事件详情
    """
    event = db.query(BusinessEvent).filter(
        BusinessEvent.id == event_id,
        BusinessEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")
    
    return BusinessEventResponse.model_validate(event)
