from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from kernel.models.ledger import LedgerAccount, LedgerEntry

class LedgerService(ABC):
    """账本服务接口 - Kernel层核心服务"""
    
    @abstractmethod
    def create_ledger_account(self, db: Session, account_data: Dict[str, Any]) -> LedgerAccount:
        """创建分类账"""
        pass
    
    @abstractmethod
    def get_ledger_account(self, db: Session, account_id: int, shop_id: int) -> LedgerAccount:
        """获取分类账详情"""
        pass
    
    @abstractmethod
    def list_ledger_accounts(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[LedgerAccount]:
        """获取分类账列表"""
        pass
    
    @abstractmethod
    def create_ledger_entry(self, db: Session, entry_data: Dict[str, Any]) -> LedgerEntry:
        """创建账务分录"""
        pass
    
    @abstractmethod
    def get_ledger_entries(self, db: Session, shop_id: int, filters: Dict[str, Any] = None) -> List[LedgerEntry]:
        """获取账务分录列表"""
        pass
    
    @abstractmethod
    def get_account_balance(self, db: Session, account_id: int, shop_id: int) -> float:
        """获取账户余额"""
        pass