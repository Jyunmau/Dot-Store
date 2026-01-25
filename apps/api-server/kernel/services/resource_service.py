from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from kernel.models.resource import Resource
from kernel.models.event import Event

class ResourceService(ABC):
    """资源服务接口 - Kernel层核心服务"""
    
    @abstractmethod
    def create_resource(self, db: Session, resource_data: Dict[str, Any]) -> Resource:
        """创建资源"""
        pass
    
    @abstractmethod
    def get_resource(self, db: Session, resource_id: int, shop_id: int) -> Resource:
        """获取资源详情"""
        pass
    
    @abstractmethod
    def update_resource(self, db: Session, resource_id: int, shop_id: int, resource_data: Dict[str, Any]) -> Resource:
        """更新资源"""
        pass
    
    @abstractmethod
    def list_resources(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[Resource]:
        """获取资源列表"""
        pass
    
    @abstractmethod
    def create_resource_event(self, db: Session, event_data: Dict[str, Any]) -> Event:
        """创建资源事件"""
        pass
    
    @abstractmethod
    def get_resource_events(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[Event]:
        """获取资源事件列表"""
        pass