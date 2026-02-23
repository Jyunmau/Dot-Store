"""
Dot-Store V2.2 客户账户服务
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models.customer_account import CustomerAccount, CustomerTransaction, TransactionType
from ..services.event_service import EventService


class CustomerAccountService:
    """
    客户账户服务类
    提供客户账户管理、充值、消费等功能
    """

    @staticmethod
    def generate_transaction_no(db: Session, user_id: int, prefix: str = 'C') -> str:
        """
        生成交易编号
        格式：前缀 + 日期(YYYYMMDD) + 4位序号
        前缀：C-充值，X-消费，R-退款，A-调整
        """
        today = date.today()
        date_prefix = f"{prefix}{today.strftime('%Y%m%d')}"
        
        last_transaction = db.query(CustomerTransaction).filter(
            CustomerTransaction.transaction_no.like(f"{date_prefix}%")
        ).order_by(CustomerTransaction.transaction_no.desc()).first()
        
        if last_transaction:
            last_seq = int(last_transaction.transaction_no[-4:])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        
        return f"{date_prefix}{new_seq:04d}"

    @staticmethod
    def create_account(
        db: Session,
        user_id: int,
        customer_name: str,
        phone: str,
        operator_id: int = None,
        ip_address: str = None
    ) -> CustomerAccount:
        """
        创建客户账户
        """
        existing = db.query(CustomerAccount).filter(
            CustomerAccount.user_id == user_id,
            CustomerAccount.phone == phone
        ).first()
        
        if existing:
            raise ValueError("该手机号已存在客户账户")
        
        account = CustomerAccount(
            user_id=user_id,
            customer_name=customer_name,
            phone=phone,
            balance=Decimal('0'),
            total_recharged=Decimal('0'),
            total_consumed=Decimal('0'),
            status='active'
        )
        
        db.add(account)
        db.commit()
        db.refresh(account)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='customer_account_created',
            operator_id=operator_id or user_id,
            entity_type='customer_account',
            entity_id=account.id,
            data={
                'customer_name': customer_name,
                'phone': phone
            },
            ip_address=ip_address
        )
        
        return account

    @staticmethod
    def get_account(db: Session, user_id: int, account_id: int) -> Optional[CustomerAccount]:
        """
        获取客户账户详情
        """
        return db.query(CustomerAccount).filter(
            CustomerAccount.id == account_id,
            CustomerAccount.user_id == user_id
        ).first()

    @staticmethod
    def get_account_by_phone(db: Session, user_id: int, phone: str) -> Optional[CustomerAccount]:
        """
        按手机号查询客户账户
        """
        return db.query(CustomerAccount).filter(
            CustomerAccount.user_id == user_id,
            CustomerAccount.phone == phone
        ).first()

    @staticmethod
    def list_accounts(
        db: Session,
        user_id: int,
        search: str = None,
        status: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[CustomerAccount], int]:
        """
        获取客户账户列表
        """
        query = db.query(CustomerAccount).filter(CustomerAccount.user_id == user_id)
        
        if status:
            query = query.filter(CustomerAccount.status == status)
        
        if search:
            query = query.filter(or_(
                CustomerAccount.customer_name.ilike(f"%{search}%"),
                CustomerAccount.phone.ilike(f"%{search}%")
            ))
        
        total = query.count()
        accounts = query.order_by(CustomerAccount.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return accounts, total

    @staticmethod
    def update_account(
        db: Session,
        user_id: int,
        account_id: int,
        customer_name: str = None,
        status: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> CustomerAccount:
        """
        更新客户账户信息
        """
        account = db.query(CustomerAccount).filter(
            CustomerAccount.id == account_id,
            CustomerAccount.user_id == user_id
        ).first()
        
        if not account:
            raise ValueError("客户账户不存在")
        
        if customer_name is not None:
            account.customer_name = customer_name
        if status is not None:
            account.status = status
        
        account.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(account)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='customer_account_updated',
            operator_id=operator_id or user_id,
            entity_type='customer_account',
            entity_id=account.id,
            data={
                'customer_name': account.customer_name,
                'status': account.status
            },
            ip_address=ip_address
        )
        
        return account

    @staticmethod
    def recharge(
        db: Session,
        user_id: int,
        account_id: int,
        amount: Decimal,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> CustomerTransaction:
        """
        客户充值
        使用数据库事务保证原子性
        """
        if amount <= 0:
            raise ValueError("充值金额必须大于0")
        
        account = db.query(CustomerAccount).filter(
            CustomerAccount.id == account_id,
            CustomerAccount.user_id == user_id
        ).with_for_update().first()
        
        if not account:
            raise ValueError("客户账户不存在")
        
        if account.status != 'active':
            raise ValueError("账户状态异常，无法充值")
        
        balance_before = account.balance
        account.balance = balance_before + amount
        account.total_recharged = account.total_recharged + amount
        account.version = account.version + 1
        account.updated_at = datetime.utcnow()
        
        transaction_no = CustomerAccountService.generate_transaction_no(db, user_id, 'C')
        
        transaction = CustomerTransaction(
            user_id=user_id,
            account_id=account_id,
            transaction_no=transaction_no,
            transaction_type=TransactionType.RECHARGE.value,
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
            event_type='customer_recharge',
            operator_id=operator_id or user_id,
            entity_type='customer_account',
            entity_id=account_id,
            data={
                'amount': float(amount),
                'transaction_no': transaction_no,
                'balance_after': float(account.balance)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def consume(
        db: Session,
        user_id: int,
        account_id: int,
        amount: Decimal,
        order_id: int = None,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> CustomerTransaction:
        """
        客户消费
        使用数据库事务保证原子性
        """
        if amount <= 0:
            raise ValueError("消费金额必须大于0")
        
        account = db.query(CustomerAccount).filter(
            CustomerAccount.id == account_id,
            CustomerAccount.user_id == user_id
        ).with_for_update().first()
        
        if not account:
            raise ValueError("客户账户不存在")
        
        if account.status != 'active':
            raise ValueError("账户状态异常。无法消费")
        
        if account.balance < amount:
            raise ValueError("余额不足")
        
        balance_before = account.balance
        account.balance = balance_before - amount
        account.total_consumed = account.total_consumed + amount
        account.version = account.version + 1
        account.updated_at = datetime.utcnow()
        
        transaction_no = CustomerAccountService.generate_transaction_no(db, user_id, 'X')
        
        transaction = CustomerTransaction(
            user_id=user_id,
            account_id=account_id,
            transaction_no=transaction_no,
            transaction_type=TransactionType.CONSUME.value,
            amount=amount,
            balance_before=balance_before,
            balance_after=account.balance,
            order_id=order_id,
            note=note,
            operator_id=operator_id or user_id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='customer_consume',
            operator_id=operator_id or user_id,
            entity_type='customer_account',
            entity_id=account_id,
            data={
                'amount': float(amount),
                'transaction_no': transaction_no,
                'order_id': order_id,
                'balance_after': float(account.balance)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def get_transactions(
        db: Session,
        user_id: int,
        account_id: int,
        transaction_type: str = None,
        start_date: date = None,
        end_date: date = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[CustomerTransaction], int]:
        """
        获取客户交易记录
        """
        query = db.query(CustomerTransaction).filter(
            CustomerTransaction.user_id == user_id,
            CustomerTransaction.account_id == account_id
        )
        
        if transaction_type:
            query = query.filter(CustomerTransaction.transaction_type == transaction_type)
        
        if start_date:
            query = query.filter(CustomerTransaction.created_at >= start_date)
        if end_date:
            next_day = date(end_date.year, end_date.month, end_date.day + 1)
            query = query.filter(CustomerTransaction.created_at < next_day)
        
        total = query.count()
        transactions = query.order_by(CustomerTransaction.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return transactions, total

    @staticmethod
    def rebuild_balance(db: Session, user_id: int, account_id: int) -> Tuple[Decimal, Decimal, bool]:
        """
        从交易记录重建余额
        用于数据校验和修复
        返回：(原余额, 计算余额, 是否一致)
        """
        account = db.query(CustomerAccount).filter(
            CustomerAccount.id == account_id,
            CustomerAccount.user_id == user_id
        ).first()
        
        if not account:
            raise ValueError("客户账户不存在")
        
        transactions = db.query(CustomerTransaction).filter(
            CustomerTransaction.account_id == account_id
        ).all()
        
        calculated_balance = Decimal('0')
        
        for t in transactions:
            if t.transaction_type in [TransactionType.RECHARGE.value, TransactionType.REFUND.value, TransactionType.ADJUST_ADD.value]:
                calculated_balance += t.amount
            elif t.transaction_type in [TransactionType.CONSUME.value, TransactionType.ADJUST_SUB.value]:
                calculated_balance -= t.amount
        
        original_balance = account.balance
        is_consistent = abs(original_balance - calculated_balance) < Decimal('0.01')
        
        if not is_consistent:
            account.balance = calculated_balance
            account.version = account.version + 1
            account.updated_at = datetime.utcnow()
            db.commit()
        
        return original_balance, calculated_balance, is_consistent
