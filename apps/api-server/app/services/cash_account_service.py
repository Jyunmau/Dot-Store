"""
Dot-Store V2.2 现金账户服务
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Tuple, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from ..models.cash_account import CashAccount, CashTransaction, CashTransactionType, INCOME_CATEGORIES, EXPENSE_CATEGORIES
from ..services.event_service import EventService


class CashAccountService:
    """
    现金账户服务类
    提供现金账户管理、收支记录等功能
    """

    @staticmethod
    def generate_transaction_no(db: Session, user_id: int, prefix: str = 'I') -> str:
        """
        生成交易编号
        格式：前缀 + 日期(YYYYMMDD) + 4位序号
        前缀：I-收入，E-支出，T-转账，A-调整
        """
        today = date.today()
        date_prefix = f"{prefix}{today.strftime('%Y%m%d')}"
        
        last_transaction = db.query(CashTransaction).filter(
            CashTransaction.transaction_no.like(f"{date_prefix}%")
        ).order_by(CashTransaction.transaction_no.desc()).first()
        
        if last_transaction:
            last_seq = int(last_transaction.transaction_no[-4:])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        
        return f"{date_prefix}{new_seq:04d}"

    @staticmethod
    def get_or_create_account(db: Session, user_id: int) -> CashAccount:
        """
        获取或创建现金账户
        每个用户只有一个现金账户
        """
        account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        
        if not account:
            account = CashAccount(
                user_id=user_id,
                account_name="主账户",
                account_type="cash",
                balance=Decimal('0'),
                total_income=Decimal('0'),
                total_expense=Decimal('0'),
                status='active'
            )
            db.add(account)
            db.commit()
            db.refresh(account)
            
            EventService.log(
                db=db,
                user_id=user_id,
                event_type='cash_account_created',
                operator_id=user_id,
                entity_type='cash_account',
                entity_id=account.id,
                data={'account_name': '主账户'}
            )
        
        return account

    @staticmethod
    def get_account(db: Session, user_id: int) -> Optional[CashAccount]:
        """
        获取现金账户
        """
        return CashAccountService.get_or_create_account(db, user_id)

    @staticmethod
    def update_account(
        db: Session,
        user_id: int,
        account_name: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> CashAccount:
        """
        更新现金账户信息
        """
        account = CashAccountService.get_or_create_account(db, user_id)
        
        if account_name is not None:
            account.account_name = account_name
        
        account.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(account)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='cash_account_updated',
            operator_id=operator_id or user_id,
            entity_type='cash_account',
            entity_id=account.id,
            data={'account_name': account.account_name},
            ip_address=ip_address
        )
        
        return account

    @staticmethod
    def record_income(
        db: Session,
        user_id: int,
        amount: Decimal,
        category: str,
        order_id: int = None,
        customer_transaction_id: int = None,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> CashTransaction:
        """
        记录收入
        使用数据库事务保证原子性
        """
        if amount <= 0:
            raise ValueError("收入金额必须大于0")
        
        valid_categories = [c[0] for c in INCOME_CATEGORIES]
        if category not in valid_categories:
            raise ValueError(f"无效的收入分类。有效分类：{valid_categories}")
        
        account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).with_for_update().first()
        
        if not account:
            account = CashAccountService.get_or_create_account(db, user_id)
            account = db.query(CashAccount).filter(
                CashAccount.user_id == user_id
            ).with_for_update().first()
        
        if account.status != 'active':
            raise ValueError("账户状态异常。无法记录收入")
        
        balance_before = account.balance
        account.balance = balance_before + amount
        account.total_income = account.total_income + amount
        account.version = account.version + 1
        account.updated_at = datetime.utcnow()
        
        transaction_no = CashAccountService.generate_transaction_no(db, user_id, 'I')
        
        transaction = CashTransaction(
            user_id=user_id,
            account_id=account.id,
            transaction_no=transaction_no,
            transaction_type=CashTransactionType.INCOME.value,
            category=category,
            amount=amount,
            balance_before=balance_before,
            balance_after=account.balance,
            order_id=order_id,
            customer_transaction_id=customer_transaction_id,
            note=note,
            operator_id=operator_id or user_id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='cash_income',
            operator_id=operator_id or user_id,
            entity_type='cash_account',
            entity_id=account.id,
            data={
                'amount': float(amount),
                'category': category,
                'transaction_no': transaction_no,
                'balance_after': float(account.balance)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def record_expense(
        db: Session,
        user_id: int,
        amount: Decimal,
        category: str,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> CashTransaction:
        """
        记录支出
        使用数据库事务保证原子性
        """
        if amount <= 0:
            raise ValueError("支出金额必须大于0")
        
        valid_categories = [c[0] for c in EXPENSE_CATEGORIES]
        if category not in valid_categories:
            raise ValueError(f"无效的支出分类。有效分类：{valid_categories}")
        
        account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).with_for_update().first()
        
        if not account:
            account = CashAccountService.get_or_create_account(db, user_id)
            account = db.query(CashAccount).filter(
                CashAccount.user_id == user_id
            ).with_for_update().first()
        
        if account.status != 'active':
            raise ValueError("账户状态异常。无法记录支出")
        
        if account.balance < amount:
            raise ValueError("余额不足")
        
        balance_before = account.balance
        account.balance = balance_before - amount
        account.total_expense = account.total_expense + amount
        account.version = account.version + 1
        account.updated_at = datetime.utcnow()
        
        transaction_no = CashAccountService.generate_transaction_no(db, user_id, 'E')
        
        transaction = CashTransaction(
            user_id=user_id,
            account_id=account.id,
            transaction_no=transaction_no,
            transaction_type=CashTransactionType.EXPENSE.value,
            category=category,
            amount=amount,
            balance_before=balance_before,
            balance_after=account.balance,
            note=note,
            operator_id=operator_id or user_id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='cash_expense',
            operator_id=operator_id or user_id,
            entity_type='cash_account',
            entity_id=account.id,
            data={
                'amount': float(amount),
                'category': category,
                'transaction_no': transaction_no,
                'balance_after': float(account.balance)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def get_transactions(
        db: Session,
        user_id: int,
        start_date: date = None,
        end_date: date = None,
        transaction_type: str = None,
        category: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[CashTransaction], int]:
        """
        获取现金交易记录
        """
        account = CashAccountService.get_or_create_account(db, user_id)
        
        query = db.query(CashTransaction).filter(
            CashTransaction.user_id == user_id,
            CashTransaction.account_id == account.id
        )
        
        if transaction_type:
            query = query.filter(CashTransaction.transaction_type == transaction_type)
        
        if category:
            query = query.filter(CashTransaction.category == category)
        
        if start_date:
            query = query.filter(CashTransaction.created_at >= start_date)
        if end_date:
            next_day = date(end_date.year, end_date.month, end_date.day + 1)
            query = query.filter(CashTransaction.created_at < next_day)
        
        total = query.count()
        transactions = query.order_by(CashTransaction.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return transactions, total

    @staticmethod
    def get_summary(
        db: Session,
        user_id: int,
        start_date: date = None,
        end_date: date = None
    ) -> Dict:
        """
        获取收支汇总
        """
        account = CashAccountService.get_or_create_account(db, user_id)
        
        query = db.query(CashTransaction).filter(
            CashTransaction.user_id == user_id,
            CashTransaction.account_id == account.id
        )
        
        if start_date:
            query = query.filter(CashTransaction.created_at >= start_date)
        if end_date:
            next_day = date(end_date.year, end_date.month, end_date.day + 1)
            query = query.filter(CashTransaction.created_at < next_day)
        
        transactions = query.all()
        
        total_income = Decimal('0')
        total_expense = Decimal('0')
        categories: Dict[str, Decimal] = {}
        
        for t in transactions:
            if t.transaction_type == CashTransactionType.INCOME.value:
                total_income += t.amount
            elif t.transaction_type == CashTransactionType.EXPENSE.value:
                total_expense += t.amount
            
            if t.category not in categories:
                categories[t.category] = Decimal('0')
            if t.transaction_type == CashTransactionType.INCOME.value:
                categories[t.category] += t.amount
            elif t.transaction_type == CashTransactionType.EXPENSE.value:
                categories[t.category] -= t.amount
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_income': total_income - total_expense,
            'categories': {k: float(v) for k, v in categories.items()}
        }

    @staticmethod
    def rebuild_balance(db: Session, user_id: int) -> Tuple[Decimal, Decimal, bool]:
        """
        从交易记录重建余额
        用于数据校验和修复
        返回：(原余额, 计算余额, 是否一致)
        """
        account = CashAccountService.get_or_create_account(db, user_id)
        
        transactions = db.query(CashTransaction).filter(
            CashTransaction.account_id == account.id
        ).all()
        
        calculated_balance = Decimal('0')
        
        for t in transactions:
            if t.transaction_type in [CashTransactionType.INCOME.value, CashTransactionType.TRANSFER_IN.value, CashTransactionType.ADJUST_ADD.value]:
                calculated_balance += t.amount
            elif t.transaction_type in [CashTransactionType.EXPENSE.value, CashTransactionType.TRANSFER_OUT.value, CashTransactionType.ADJUST_SUB.value]:
                calculated_balance -= t.amount
        
        original_balance = account.balance
        is_consistent = abs(original_balance - calculated_balance) < Decimal('0.01')
        
        if not is_consistent:
            account.balance = calculated_balance
            account.version = account.version + 1
            account.updated_at = datetime.utcnow()
            db.commit()
        
        return original_balance, calculated_balance, is_consistent
