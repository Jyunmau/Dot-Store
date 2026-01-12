from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from shared.db.base import Base

class Config(Base):
    """配置模型 - 用于承载低频但必要的可配置项"""
    __tablename__ = "configs"
    
    id = Column(BigInteger, primary_key=True, index=True)
    shop_id = Column(BigInteger, nullable=False, index=True)
    key = Column(String(64), nullable=False, index=True)
    value = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Config(id={self.id}, shop_id={self.shop_id}, key={self.key})>"

# 在 shared 目录下创建 shop 模型
class Shop(Base):
    """店铺模型"""
    __tablename__ = "shops"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    status = Column(String(32), default="active")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Shop(id={self.id}, name={self.name}, status={self.status})>"
