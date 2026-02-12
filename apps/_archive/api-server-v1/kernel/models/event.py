from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from .base import Base

class Event(Base):
    """事件模型 - 最底层事实记录，增强可扩展性支持与Resource集成"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    # 扩展字段：支持与Resource集成，不直接绑定Resource
    related_resource_id = Column(Integer, nullable=True, index=True)  # 关联的资源ID
    related_resource_type = Column(String(64), nullable=True)  # 关联的资源类型
    actor_id = Column(Integer, nullable=True, index=True)  # 执行该事件的参与者ID
    actor_type = Column(String(64), nullable=True)  # 执行该事件的参与者类型
    payload = Column(JSON)  # 事件负载，保持向后兼容
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<Event(id={self.id}, shop_id={self.shop_id}, event_type={self.event_type}, related_resource_id={self.related_resource_id})>"