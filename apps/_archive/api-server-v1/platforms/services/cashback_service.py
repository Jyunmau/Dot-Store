from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from platforms.models.cashback import CashbackPolicy, CashbackRecord, RedemptionRecord

class CashbackService(ABC):
    """返现服务接口 - Platform层核心服务"""
    
    @abstractmethod
    def create_cashback_policy(self, db: Session, policy_data: Dict[str, Any]) -> CashbackPolicy:
        """创建返现规则"""
        pass
    
    @abstractmethod
    def get_cashback_policy(self, db: Session, policy_id: int, shop_id: int) -> CashbackPolicy:
        """获取返现规则详情"""
        pass
    
    @abstractmethod
    def list_cashback_policies(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[CashbackPolicy]:
        """获取返现规则列表"""
        pass
    
    @abstractmethod
    def calculate_cashback(self, db: Session, order_data: Dict[str, Any], member_id: int = None) -> Dict[str, Any]:
        """计算返现金额"""
        pass
    
    @abstractmethod
    def process_cashback(self, db: Session, order_id: int, shop_id: int) -> CashbackRecord:
        """处理返现"""
        pass
    
    @abstractmethod
    def get_cashback_history(self, db: Session, member_id: int, shop_id: int, filters: Dict[str, Any] = None) -> List[CashbackRecord]:
        """获取返现历史"""
        pass