"""
Dot-Store V2.2 事件日志服务
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.business_event import BusinessEvent
from ..schemas.event import EventCategory, EventType


class EventService:
    """
    事件日志服务类
    """
    
    EVENT_CATEGORY_MAP = {
        EventType.USER_LOGIN: EventCategory.AUTH,
        EventType.USER_LOGOUT: EventCategory.AUTH,
        EventType.USER_REGISTER: EventCategory.AUTH,
        EventType.API_KEY_GENERATED: EventCategory.AUTH,
        EventType.ORDER_CREATED: EventCategory.ORDER,
        EventType.ORDER_UPDATED: EventCategory.ORDER,
        EventType.ORDER_VOIDED: EventCategory.ORDER,
        EventType.STOCK_IN: EventCategory.STOCK,
        EventType.STOCK_OUT: EventCategory.STOCK,
        EventType.STOCK_ADJUST: EventCategory.STOCK,
        EventType.INGREDIENT_CREATED: EventCategory.STOCK,
        EventType.CUSTOMER_CREATED: EventCategory.CUSTOMER,
        EventType.CUSTOMER_RECHARGE: EventCategory.CUSTOMER,
        EventType.CUSTOMER_CONSUME: EventCategory.CUSTOMER,
        EventType.CASH_INCOME: EventCategory.CASH,
        EventType.CASH_EXPENSE: EventCategory.CASH,
        EventType.FINANCIAL_SNAPSHOT_CREATED: EventCategory.FINANCE,
        EventType.BACKUP_CREATED: EventCategory.SYSTEM,
        EventType.BACKUP_RESTORED: EventCategory.SYSTEM,
        EventType.MCP_TOOL_CALLED: EventCategory.MCP,
        EventType.MCP_RESOURCE_ACCESSED: EventCategory.MCP,
    }

    @staticmethod
    def get_event_category(event_type: str) -> str:
        """
        根据事件类型获取事件分类
        """
        try:
            event_type_enum = EventType(event_type)
            return EventService.EVENT_CATEGORY_MAP.get(event_type_enum, EventCategory.SYSTEM).value
        except ValueError:
            return EventCategory.SYSTEM.value

    @staticmethod
    def log(
        db: Session,
        user_id: int,
        event_type: str,
        operator_id: int,
        operator_type: str = 'user',
        entity_type: str = None,
        entity_id: int = None,
        data: dict = None,
        ip_address: str = None,
        user_agent: str = None
    ) -> BusinessEvent:
        """
        记录业务事件
        """
        event_category = EventService.get_event_category(event_type)
        
        event = BusinessEvent(
            user_id=user_id,
            event_type=event_type,
            event_category=event_category,
            entity_type=entity_type,
            entity_id=entity_id,
            operator_id=operator_id,
            operator_type=operator_type,
            data=data,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow()
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        return event

    @staticmethod
    def get_events(
        db: Session,
        user_id: int,
        start_date: date = None,
        end_date: date = None,
        event_type: str = None,
        event_category: str = None,
        entity_type: str = None,
        entity_id: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple:
        """
        获取事件列表
        """
        query = db.query(BusinessEvent).filter(BusinessEvent.user_id == user_id)
        
        if start_date:
            query = query.filter(BusinessEvent.created_at >= start_date)
        if end_date:
            query = query.filter(BusinessEvent.created_at < end_date)
        if event_type:
            query = query.filter(BusinessEvent.event_type == event_type)
        if event_category:
            query = query.filter(BusinessEvent.event_category == event_category)
        if entity_type:
            query = query.filter(BusinessEvent.entity_type == entity_type)
        if entity_id:
            query = query.filter(BusinessEvent.entity_id == entity_id)
        
        total = query.count()
        events = query.order_by(BusinessEvent.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return events, total

    @staticmethod
    def get_entity_events(
        db: Session,
        user_id: int,
        entity_type: str,
        entity_id: int
    ) -> List[BusinessEvent]:
        """
        获取实体相关事件
        """
        return db.query(BusinessEvent).filter(
            and_(
                BusinessEvent.user_id == user_id,
                BusinessEvent.entity_type == entity_type,
                BusinessEvent.entity_id == entity_id
            )
        ).order_by(BusinessEvent.created_at.desc()).all()
