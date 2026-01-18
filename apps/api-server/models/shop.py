from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base

class Shop(Base):
    """店铺模型"""
    __tablename__ = "shops"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    status = Column(String(32), default="active")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Shop(id={self.id}, name={self.name}, status={self.status})>"
