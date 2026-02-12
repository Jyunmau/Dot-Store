"""
Dot-Store V2.1 收支记录服务层
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.transaction import Transaction, TransactionCategory
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionFilters,
)


class TransactionService:
    """
    收支记录服务类
    """

    def __init__(self, db: Session):
        """
        初始化收支记录服务
        """
        self.db = db

    def create_transaction(
        self, user_id: int, transaction_data: TransactionCreate, created_by: int
    ) -> Transaction:
        """
        创建收支记录
        
        Args:
            user_id: 用户ID
            transaction_data: 收支记录创建数据
            created_by: 创建人ID
            
        Returns:
            Transaction: 创建的收支记录对象
        """
        transaction = Transaction(
            user_id=user_id,
            type=transaction_data.type,
            category=transaction_data.category,
            amount=transaction_data.amount,
            order_id=transaction_data.order_id,
            note=transaction_data.note,
            attachment_url=transaction_data.attachment_url,
            created_by=created_by,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_transaction(self, transaction_id: int, user_id: int) -> Optional[Transaction]:
        """
        获取收支记录详情
        
        Args:
            transaction_id: 收支记录ID
            user_id: 用户ID
            
        Returns:
            Transaction: 收支记录对象，不存在则返回None
        """
        return self.db.query(Transaction).filter(
            and_(Transaction.id == transaction_id, Transaction.user_id == user_id)
        ).first()

    def list_transactions(
        self, user_id: int, filters: Optional[TransactionFilters] = None
    ) -> dict:
        """
        获取收支记录列表
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            
        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)

        if filters:
            if filters.start_date:
                query = query.filter(Transaction.created_at >= filters.start_date)
            if filters.end_date:
                query = query.filter(Transaction.created_at <= filters.end_date)
            if filters.type:
                query = query.filter(Transaction.type == filters.type)
            if filters.category:
                query = query.filter(Transaction.category == filters.category)

        total = query.count()

        page = filters.page if filters else 1
        page_size = filters.page_size if filters else 10
        offset = (page - 1) * page_size

        transactions = (
            query.order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return {
            "items": transactions,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def update_transaction(
        self, transaction_id: int, user_id: int, transaction_data: TransactionUpdate
    ) -> Optional[Transaction]:
        """
        更新收支记录
        
        Args:
            transaction_id: 收支记录ID
            user_id: 用户ID
            transaction_data: 收支记录更新数据
            
        Returns:
            Transaction: 更新后的收支记录对象，不存在则返回None
        """
        transaction = self.get_transaction(transaction_id, user_id)
        if not transaction:
            return None

        update_data = transaction_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(transaction, key, value)

        transaction.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        """
        删除收支记录
        
        Args:
            transaction_id: 收支记录ID
            user_id: 用户ID
            
        Returns:
            bool: 删除成功返回True，收支记录不存在返回False
        """
        transaction = self.get_transaction(transaction_id, user_id)
        if not transaction:
            return False

        self.db.delete(transaction)
        self.db.commit()
        return True

    def get_transaction_summary(
        self, user_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> dict:
        """
        获取收支汇总统计
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            dict: 包含income, expense, net_profit, categories的字典
        """
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.created_at >= start_date)
        if end_date:
            query = query.filter(Transaction.created_at <= end_date)

        transactions = query.all()

        income = Decimal("0")
        expense = Decimal("0")
        categories: Dict[str, Decimal] = {}

        for t in transactions:
            amount = t.amount
            if t.type == "income":
                income += amount
                if t.category in categories:
                    categories[t.category] += amount
                else:
                    categories[t.category] = amount
            elif t.type == "expense":
                expense += amount
                if t.category in categories:
                    categories[t.category] -= amount
                else:
                    categories[t.category] = -amount

        net_profit = income - expense

        return {
            "income": income,
            "expense": expense,
            "net_profit": net_profit,
            "categories": {k: v for k, v in categories.items() if v != 0},
        }

    def get_categories_by_type(self, user_id: int, type: Optional[str] = None) -> List[str]:
        """
        获取用户所有收支分类名称
        
        Args:
            user_id: 用户ID
            type: 类型筛选（income/expense）
            
        Returns:
            List[str]: 分类名称列表
        """
        query = self.db.query(Transaction.category).filter(
            Transaction.user_id == user_id
        )
        
        if type:
            query = query.filter(Transaction.type == type)
            
        result = query.distinct().all()
        return [r[0] for r in result]

    def batch_create_transactions(
        self, user_id: int, transactions_data: List[TransactionCreate], created_by: int
    ) -> List[Transaction]:
        """
        批量创建收支记录
        
        Args:
            user_id: 用户ID
            transactions_data: 收支记录创建数据列表
            created_by: 创建人ID
            
        Returns:
            List[Transaction]: 创建的收支记录列表
        """
        transactions = []
        for data in transactions_data:
            transaction = Transaction(
                user_id=user_id,
                type=data.type,
                category=data.category,
                amount=data.amount,
                order_id=data.order_id,
                note=data.note,
                attachment_url=data.attachment_url,
                created_by=created_by,
            )
            transactions.append(transaction)
            self.db.add(transaction)
        
        self.db.commit()
        for t in transactions:
            self.db.refresh(t)
        return transactions
