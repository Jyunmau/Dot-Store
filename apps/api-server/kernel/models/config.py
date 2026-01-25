from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from .base import Base

class Config(Base):
    """配置模型 - 用于承载低频但必要的可配置项"""
    __tablename__ = "configs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    key = Column(String(64), nullable=False, index=True)
    value = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Config(id={self.id}, shop_id={self.shop_id}, key={self.key})>"