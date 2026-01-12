from sqlalchemy import Column, BigInteger, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from .base import Base

class Event(Base):
    """事件模型 - 最底层事实记录"""
    __tablename__ = "events"
    
    id = Column(BigInteger, primary_key=True, index=True)
    shop_id = Column(BigInteger, nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    payload = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<Event(id={self.id}, shop_id={self.shop_id}, event_type={self.event_type})>"
