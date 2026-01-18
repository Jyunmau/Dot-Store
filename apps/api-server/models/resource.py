from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Resource(Base):
    """抽象资源管理模型 - Kernel层核心模块"""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    resource_type = Column(String(64), nullable=False, index=True)  # 资源类型：table, booth, etc.
    name = Column(String(128), nullable=True)  # 资源名称
    resource_metadata = Column(JSON, nullable=True)  # 资源元数据，用于存储行业特定属性（避免使用保留关键字）
    # 状态字段：通过ResourceEvent计算得出，不在数据库中直接存储
    
    # 与Event的关系：事件可以关联到资源，但资源不直接管理事件
    # 这种设计确保了Resource与Event的松耦合，符合Kernel层设计原则
    
    def __repr__(self):
        return f"<Resource(id={self.id}, shop_id={self.shop_id}, resource_type={self.resource_type}, name={self.name})>"
