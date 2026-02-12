from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from platforms.models.reservation import Reservation
from platforms.models.table import Table

class ReservationService(ABC):
    """订台服务接口 - Platform层核心服务"""
    
    @abstractmethod
    def create_reservation(self, db: Session, reservation_data: Dict[str, Any]) -> Reservation:
        """创建订台"""
        pass
    
    @abstractmethod
    def get_reservation(self, db: Session, reservation_id: int, shop_id: int) -> Reservation:
        """获取订台详情"""
        pass
    
    @abstractmethod
    def update_reservation_status(self, db: Session, reservation_id: int, shop_id: int, status: str) -> Reservation:
        """更新订台状态"""
        pass
    
    @abstractmethod
    def list_reservations(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[Reservation]:
        """获取订台列表"""
        pass
    
    @abstractmethod
    def get_available_tables(self, db: Session, shop_id: int, start_time: str, end_time: str, people_count: int) -> List[Table]:
        """获取可用酒台列表"""
        pass
    
    @abstractmethod
    def cancel_reservation(self, db: Session, reservation_id: int, shop_id: int, reason: str = None) -> Reservation:
        """取消订台"""
        pass