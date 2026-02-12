from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from kernel.models.account import Account

class AccountService(ABC):
    """账户服务接口 - Kernel层核心服务"""
    
    @abstractmethod
    def create_account(self, db: Session, account_data: Dict[str, Any]) -> Account:
        """创建账户"""
        pass
    
    @abstractmethod
    def get_account(self, db: Session, account_id: int, shop_id: int) -> Account:
        """获取账户详情"""
        pass
    
    @abstractmethod
    def update_account(self, db: Session, account_id: int, shop_id: int, account_data: Dict[str, Any]) -> Account:
        """更新账户"""
        pass
    
    @abstractmethod
    def list_accounts(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[Account]:
        """获取账户列表"""
        pass
    
    @abstractmethod
    def authenticate_account(self, db: Session, identifier: str, password: str) -> Dict[str, Any]:
        """认证账户"""
        pass