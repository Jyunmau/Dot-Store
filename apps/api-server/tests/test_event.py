import pytest
from sqlalchemy.orm import Session
from models.event import Event
from models.database import get_db
from main import app
from fastapi.testclient import TestClient
from conftest import db

@pytest.fixture(scope="function")
def client(db):
    return TestClient(app)

# 测试Event模型
def test_event_model(db: Session):
    """测试Event模型的创建和基本属性"""
    event = Event(
        shop_id=1,
        event_type="test_event",
        payload={"test_key": "test_value"},
        related_resource_id=1,
        related_resource_type="test_resource",
        actor_id=1,
        actor_type="test_actor"
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    assert event.id is not None
    assert event.shop_id == 1
    assert event.event_type == "test_event"
    assert event.payload == {"test_key": "test_value"}
    assert event.related_resource_id == 1
    assert event.related_resource_type == "test_resource"
    assert event.actor_id == 1
    assert event.actor_type == "test_actor"
    assert event.created_at is not None

# 测试Event API
def test_create_event(client):
    """测试创建Event的API"""
    event_data = {
        "shop_id": 1,
        "event_type": "test_api_event",
        "payload": {"api_key": "api_value"},
        "actor_id": 1,
        "actor_type": "test_actor"
    }
    
    response = client.post("/api/resource-events", json=event_data)
    
    assert response.status_code == 200
    assert response.json()["message"] == "资源事件创建成功"
    assert "id" in response.json()

# 测试获取Event API
def test_get_event(client):
    """测试获取Event的API"""
    # 先创建一个event
    event_data = {
        "shop_id": 1,
        "event_type": "test_get_event",
        "payload": {"get_key": "get_value"}
    }
    create_response = client.post("/api/resource-events", json=event_data)
    event_id = create_response.json()["id"]
    
    # 然后获取该event
    get_response = client.get(f"/api/resource-events/{event_id}")
    
    assert get_response.status_code == 200
    assert get_response.json()["id"] == event_id
    assert get_response.json()["event_type"] == "test_get_event"
    assert get_response.json()["payload"] == {"get_key": "get_value"}

# 测试获取Event列表API
def test_get_events(client):
    """测试获取Event列表的API"""
    response = client.get("/api/resource-events?shop_id=1")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
