from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from platforms.models.member import Member

class MemberService(ABC):
    """会员服务接口 - Platform层核心服务"""
    
    @abstractmethod
    def create_member(self, db: Session, member_data: Dict[str, Any]) -> Member:
        """创建会员"""
        pass
    
    @abstractmethod
    def get_member(self, db: Session, member_id: int, shop_id: int) -> Member:
        """获取会员详情"""
        pass
    
    @abstractmethod
    def update_member(self, db: Session, member_id: int, shop_id: int, member_data: Dict[str, Any]) -> Member:
        """更新会员信息"""
        pass
    
    @abstractmethod
    def list_members(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[Member]:
        """获取会员列表"""
        pass
    
    @abstractmethod
    def upgrade_member(self, db: Session, member_id: int, shop_id: int, new_level: str) -> Member:
        """升级会员等级"""
        pass
    
    @abstractmethod
    def get_member_stats(self, db: Session, member_id: int, shop_id: int) -> Dict[str, Any]:
        """获取会员统计信息"""
        pass