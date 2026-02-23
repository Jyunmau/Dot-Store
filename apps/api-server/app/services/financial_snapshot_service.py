"""
Dot-Store V2.2 财务快照服务
"""
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import List, Optional, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from ..models.financial_snapshot import FinancialSnapshot
from ..models.cash_account import CashAccount, CashTransaction
from ..models.customer_account import CustomerAccount
from ..models.stock import Ingredient
from ..models.order import Order
from ..models.expense_record import ExpenseRecord
from ..services.event_service import EventService


class FinancialSnapshotService:
    """
    财务快照服务类
    """

    @staticmethod
    def _get_or_create_cash_account(db: Session, user_id: int) -> CashAccount:
        """
        获取或创建现金账户
        """
        cash_account = db.query(CashAccount).filter(
            CashAccount.user_id == user_id
        ).first()
        
        if not cash_account:
            cash_account = CashAccount(
                user_id=user_id,
                account_name='主账户',
                account_type='cash',
                balance=Decimal('0'),
                total_income=Decimal('0'),
                total_expense=Decimal('0'),
                status='active'
            )
            db.add(cash_account)
            db.commit()
            db.refresh(cash_account)
        
        return cash_account

    @staticmethod
    def create_snapshot(
        db: Session,
        user_id: int,
        snapshot_date: date,
        snapshot_type: str = 'daily',
        operator_id: int = None,
        ip_address: str = None
    ) -> FinancialSnapshot:
        """
        创建财务快照
        """
        existing = db.query(FinancialSnapshot).filter(
            and_(
                FinancialSnapshot.user_id == user_id,
                FinancialSnapshot.snapshot_date == snapshot_date
            )
        ).first()
        
        if existing:
            raise ValueError(f"该日期({snapshot_date})已存在快照")
        
        cash_account = FinancialSnapshotService._get_or_create_cash_account(db, user_id)
        cash_balance = cash_account.balance
        
        customer_prepaid = db.query(
            func.sum(CustomerAccount.balance)
        ).filter(
            CustomerAccount.user_id == user_id,
            CustomerAccount.status == 'active'
        ).scalar() or Decimal('0')
        
        inventory_value = db.query(
            func.sum(Ingredient.current_stock * Ingredient.cost_per_unit)
        ).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active'
        ).scalar() or Decimal('0')
        
        next_day = snapshot_date + timedelta(days=1)
        daily_revenue_result = db.query(
            func.sum(CashTransaction.amount)
        ).filter(
            CashTransaction.user_id == user_id,
            CashTransaction.transaction_type == 'income',
            CashTransaction.created_at >= snapshot_date,
            CashTransaction.created_at < next_day
        ).scalar()
        daily_revenue = daily_revenue_result or Decimal('0')
        
        daily_expense_result = db.query(
            func.sum(ExpenseRecord.amount)
        ).filter(
            ExpenseRecord.user_id == user_id,
            ExpenseRecord.expense_date == snapshot_date
        ).scalar()
        daily_expense = daily_expense_result or Decimal('0')
        
        order_count = db.query(Order).filter(
            Order.user_id == user_id,
            Order.is_deleted == False,
            Order.created_at >= snapshot_date,
            Order.created_at < next_day
        ).count()
        
        snapshot = FinancialSnapshot(
            user_id=user_id,
            snapshot_date=snapshot_date,
            snapshot_type=snapshot_type,
            cash_balance=cash_balance,
            customer_prepaid=customer_prepaid,
            inventory_value=inventory_value,
            daily_revenue=daily_revenue,
            daily_expense=daily_expense,
            order_count=order_count,
            validation_status='pending'
        )
        
        snapshot.calculate_totals()
        
        validation_errors = FinancialSnapshotService.validate_snapshot(db, user_id, snapshot)
        if validation_errors:
            snapshot.validation_status = 'failed'
            snapshot.validation_errors = validation_errors
        else:
            snapshot.validation_status = 'passed'
        
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='financial_snapshot_created',
            operator_id=operator_id or user_id,
            entity_type='financial_snapshot',
            entity_id=snapshot.id,
            data={
                'snapshot_date': str(snapshot_date),
                'cash_balance': float(cash_balance),
                'inventory_value': float(inventory_value),
                'customer_prepaid': float(customer_prepaid),
                'net_assets': float(snapshot.net_assets)
            },
            ip_address=ip_address
        )
        
        return snapshot

    @staticmethod
    def validate_snapshot(db: Session, user_id: int, snapshot: FinancialSnapshot) -> Optional[Dict]:
        """
        校验快照数据完整性
        """
        errors = []
        
        if snapshot.cash_balance < 0:
            errors.append({
                'field': 'cash_balance',
                'message': '现金余额不能为负数',
                'value': float(snapshot.cash_balance)
            })
        
        if snapshot.inventory_value < 0:
            errors.append({
                'field': 'inventory_value',
                'message': '库存价值不能为负数',
                'value': float(snapshot.inventory_value)
            })
        
        if snapshot.customer_prepaid < 0:
            errors.append({
                'field': 'customer_prepaid',
                'message': '预收款不能为负数',
                'value': float(snapshot.customer_prepaid)
            })
        
        calculated_total = snapshot.cash_balance + snapshot.inventory_value
        if abs(snapshot.total_assets - calculated_total) > Decimal('0.01'):
            errors.append({
                'field': 'total_assets',
                'message': '总资产计算不一致',
                'expected': float(calculated_total),
                'actual': float(snapshot.total_assets)
            })
        
        calculated_net = snapshot.total_assets - snapshot.total_liabilities
        if abs(snapshot.net_assets - calculated_net) > Decimal('0.01'):
            errors.append({
                'field': 'net_assets',
                'message': '净资产计算不一致',
                'expected': float(calculated_net),
                'actual': float(snapshot.net_assets)
            })
        
        return {'errors': errors} if errors else None

    @staticmethod
    def get_snapshot(db: Session, user_id: int, snapshot_date: date) -> Optional[FinancialSnapshot]:
        """
        获取指定日期的快照
        """
        return db.query(FinancialSnapshot).filter(
            and_(
                FinancialSnapshot.user_id == user_id,
                FinancialSnapshot.snapshot_date == snapshot_date
            )
        ).first()

    @staticmethod
    def get_snapshot_by_id(db: Session, user_id: int, snapshot_id: int) -> Optional[FinancialSnapshot]:
        """
        获取快照详情
        """
        return db.query(FinancialSnapshot).filter(
            and_(
                FinancialSnapshot.id == snapshot_id,
                FinancialSnapshot.user_id == user_id
            )
        ).first()

    @staticmethod
    def get_snapshots(
        db: Session,
        user_id: int,
        start_date: date = None,
        end_date: date = None,
        snapshot_type: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[FinancialSnapshot], int]:
        """
        获取快照列表
        """
        query = db.query(FinancialSnapshot).filter(FinancialSnapshot.user_id == user_id)
        
        if start_date:
            query = query.filter(FinancialSnapshot.snapshot_date >= start_date)
        if end_date:
            query = query.filter(FinancialSnapshot.snapshot_date <= end_date)
        if snapshot_type:
            query = query.filter(FinancialSnapshot.snapshot_type == snapshot_type)
        
        total = query.count()
        snapshots = query.order_by(FinancialSnapshot.snapshot_date.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return snapshots, total

    @staticmethod
    def compare_snapshots(
        db: Session,
        user_id: int,
        start_date: date,
        end_date: date
    ) -> Dict:
        """
        对比两个日期的快照
        """
        start_snapshot = FinancialSnapshotService.get_snapshot(db, user_id, start_date)
        end_snapshot = FinancialSnapshotService.get_snapshot(db, user_id, end_date)
        
        result = {
            'start_date': start_date,
            'end_date': end_date,
            'start_snapshot': start_snapshot,
            'end_snapshot': end_snapshot,
            'cash_balance_change': Decimal('0'),
            'inventory_value_change': Decimal('0'),
            'customer_prepaid_change': Decimal('0'),
            'net_assets_change': Decimal('0'),
            'total_revenue': Decimal('0'),
            'total_expense': Decimal('0'),
            'total_profit': Decimal('0')
        }
        
        if start_snapshot and end_snapshot:
            result['cash_balance_change'] = end_snapshot.cash_balance - start_snapshot.cash_balance
            result['inventory_value_change'] = end_snapshot.inventory_value - start_snapshot.inventory_value
            result['customer_prepaid_change'] = end_snapshot.customer_prepaid - start_snapshot.customer_prepaid
            result['net_assets_change'] = end_snapshot.net_assets - start_snapshot.net_assets
            result['total_revenue'] = end_snapshot.daily_revenue - start_snapshot.daily_revenue
            result['total_expense'] = end_snapshot.daily_expense - start_snapshot.daily_expense
            result['total_profit'] = end_snapshot.daily_profit - start_snapshot.daily_profit
        
        return result

    @staticmethod
    def get_trends(
        db: Session,
        user_id: int,
        start_date: date,
        end_date: date
    ) -> List[Dict]:
        """
        获取财务趋势数据
        """
        snapshots = db.query(FinancialSnapshot).filter(
            FinancialSnapshot.user_id == user_id,
            FinancialSnapshot.snapshot_date >= start_date,
            FinancialSnapshot.snapshot_date <= end_date
        ).order_by(FinancialSnapshot.snapshot_date.asc()).all()
        
        return [
            {
                'snapshot_date': s.snapshot_date,
                'cash_balance': s.cash_balance,
                'inventory_value': s.inventory_value,
                'customer_prepaid': s.customer_prepaid,
                'net_assets': s.net_assets,
                'daily_revenue': s.daily_revenue,
                'daily_expense': s.daily_expense,
                'daily_profit': s.daily_profit,
                'order_count': s.order_count
            }
            for s in snapshots
        ]

    @staticmethod
    def get_or_create_today_snapshot(db: Session, user_id: int) -> FinancialSnapshot:
        """
        获取或创建今日快照
        """
        today = date.today()
        snapshot = FinancialSnapshotService.get_snapshot(db, user_id, today)
        
        if not snapshot:
            snapshot = FinancialSnapshotService.create_snapshot(
                db=db,
                user_id=user_id,
                snapshot_date=today,
                snapshot_type='daily'
            )
        
        return snapshot
