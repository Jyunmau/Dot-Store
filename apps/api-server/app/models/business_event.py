"""
Dot-Store V2.2 业务事件模型
"""
from datetime import datetime
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from ..core.database import Base


class BusinessEvent(Base):
    """
    业务事件模型 - 交易事实层
    """
    __tablename__ = "business_events"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    event_category = Column(String(32), nullable=False, index=True)
    entity_type = Column(String(64), nullable=True)
    entity_id = Column(Integer, nullable=True)
    operator_id = Column(Integer, nullable=False)
    operator_type = Column(String(32), nullable=False)
    data = Column(JSONB, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<BusinessEvent(id={self.id}, type={self.event_type}, category={self.event_category})>"
