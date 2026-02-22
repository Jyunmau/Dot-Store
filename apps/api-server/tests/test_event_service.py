"""
Dot-Store V2.2 事件日志服务测试
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.models.user import User
from app.models.business_event import BusinessEvent
from app.services.event_service import EventService
from app.schemas.event import EventType, EventCategory

Base = declarative_base()


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def test_user(db_session):
    """创建测试用户"""
    user = User(
        id=1,
        phone="13800138000",
        password_hash="hashed_password",
        shop_name="测试店铺",
        shop_type="restaurant",
        city="北京"
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_get_event_category():
    """测试根据事件类型获取事件分类"""
    category = EventService.get_event_category('order_created')
    assert category == 'order'
    
    category = EventService.get_event_category('stock_in')
    assert category == 'stock'
    
    category = EventService.get_event_category('unknown_event')
    assert category == 'system'


def test_log_event(db_session, test_user):
    """测试记录事件"""
    event = EventService.log(
        db=db_session,
        user_id=test_user.id,
        event_type='order_created',
        operator_id=test_user.id,
        entity_type='order',
        entity_id=1,
        data={'order_no': 'O20260222001', 'amount': 100.00}
    )
    
    assert event.id is not None
    assert event.event_type == 'order_created'
    assert event.event_category == 'order'
    assert event.entity_type == 'order'
    assert event.entity_id == 1


def test_get_events(db_session, test_user):
    """测试获取事件列表"""
    for i in range(5):
        EventService.log(
            db=db_session,
            user_id=test_user.id,
            event_type='order_created',
            operator_id=test_user.id,
            entity_type='order',
            entity_id=i + 1
        )
    
    events, total = EventService.get_events(
        db=db_session,
        user_id=test_user.id,
        page=1,
        page_size=10
    )
    
    assert total == 5
    assert len(events) == 5


def test_get_entity_events(db_session, test_user):
    """测试获取实体相关事件"""
    EventService.log(
        db=db_session,
        user_id=test_user.id,
        event_type='order_created',
        operator_id=test_user.id,
        entity_type='order',
        entity_id=1
    )
    EventService.log(
        db=db_session,
        user_id=test_user.id,
        event_type='order_updated',
        operator_id=test_user.id,
        entity_type='order',
        entity_id=1
    )
    
    events = EventService.get_entity_events(
        db=db_session,
        user_id=test_user.id,
        entity_type='order',
        entity_id=1
    )
    
    assert len(events) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
