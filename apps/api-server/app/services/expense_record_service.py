"""
Dot-Store V2.2 成本记录服务
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from ..models.expense_record import ExpenseRecord, EXPENSE_CATEGORIES, COST_BEHAVIORS, COST_FUNCTIONS
from ..services.event_service import EventService


class ExpenseRecordService:
    """
    成本记录服务类
    """

    @staticmethod
    def create_expense(
        db: Session,
        user_id: int,
        category: str,
        amount: Decimal,
        expense_date: date,
        description: str = None,
        cost_behavior: str = None,
        cost_function: str = None,
        metadata: dict = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> ExpenseRecord:
        """
        创建成本记录
        """
        valid_categories = [c[0] for c in EXPENSE_CATEGORIES]
        if category not in valid_categories:
            raise ValueError(f"无效的成本分类。有效分类：{valid_categories}")
        
        if cost_behavior:
            valid_behaviors = [c[0] for c in COST_BEHAVIORS]
            if cost_behavior not in valid_behaviors:
                raise ValueError(f"无效的成本行为。有效值：{valid_behaviors}")
        
        if cost_function:
            valid_functions = [c[0] for c in COST_FUNCTIONS]
            if cost_function not in valid_functions:
                raise ValueError(f"无效的成本功能。有效值：{valid_functions}")
        
        expense = ExpenseRecord(
            user_id=user_id,
            category=category,
            amount=amount,
            description=description,
            expense_date=expense_date,
            cost_behavior=cost_behavior,
            cost_function=cost_function,
            metadata=metadata
        )
        
        db.add(expense)
        db.commit()
        db.refresh(expense)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='expense_create',
            operator_id=operator_id or user_id,
            entity_type='expense_record',
            entity_id=expense.id,
            data={
                'category': category,
                'amount': float(amount),
                'expense_date': str(expense_date),
                'description': description
            },
            ip_address=ip_address
        )
        
        return expense

    @staticmethod
    def get_expense(db: Session, user_id: int, expense_id: int) -> Optional[ExpenseRecord]:
        """
        获取成本记录详情
        """
        return db.query(ExpenseRecord).filter(
            and_(
                ExpenseRecord.id == expense_id,
                ExpenseRecord.user_id == user_id
            )
        ).first()

    @staticmethod
    def get_expenses(
        db: Session,
        user_id: int,
        category: str = None,
        start_date: date = None,
        end_date: date = None,
        cost_behavior: str = None,
        cost_function: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple:
        """
        获取成本记录列表
        """
        query = db.query(ExpenseRecord).filter(ExpenseRecord.user_id == user_id)
        
        if category:
            query = query.filter(ExpenseRecord.category == category)
        if start_date:
            query = query.filter(ExpenseRecord.expense_date >= start_date)
        if end_date:
            query = query.filter(ExpenseRecord.expense_date <= end_date)
        if cost_behavior:
            query = query.filter(ExpenseRecord.cost_behavior == cost_behavior)
        if cost_function:
            query = query.filter(ExpenseRecord.cost_function == cost_function)
        
        total = query.count()
        expenses = query.order_by(ExpenseRecord.expense_date.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return expenses, total

    @staticmethod
    def update_expense(
        db: Session,
        user_id: int,
        expense_id: int,
        category: str = None,
        amount: Decimal = None,
        description: str = None,
        expense_date: date = None,
        cost_behavior: str = None,
        cost_function: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> Optional[ExpenseRecord]:
        """
        更新成本记录
        """
        expense = ExpenseRecordService.get_expense(db, user_id, expense_id)
        if not expense:
            return None
        
        if category is not None:
            valid_categories = [c[0] for c in EXPENSE_CATEGORIES]
            if category not in valid_categories:
                raise ValueError(f"无效的成本分类。有效分类：{valid_categories}")
            expense.category = category
        
        if amount is not None:
            expense.amount = amount
        
        if description is not None:
            expense.description = description
        
        if expense_date is not None:
            expense.expense_date = expense_date
        
        if cost_behavior is not None:
            valid_behaviors = [c[0] for c in COST_BEHAVIORS]
            if cost_behavior not in valid_behaviors:
                raise ValueError(f"无效的成本行为。有效值：{valid_behaviors}")
            expense.cost_behavior = cost_behavior
        
        if cost_function is not None:
            valid_functions = [c[0] for c in COST_FUNCTIONS]
            if cost_function not in valid_functions:
                raise ValueError(f"无效的成本功能。有效值：{valid_functions}")
            expense.cost_function = cost_function
        
        expense.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(expense)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='expense_update',
            operator_id=operator_id or user_id,
            entity_type='expense_record',
            entity_id=expense.id,
            data={
                'category': expense.category,
                'amount': float(expense.amount),
                'expense_date': str(expense.expense_date)
            },
            ip_address=ip_address
        )
        
        return expense

    @staticmethod
    def delete_expense(
        db: Session,
        user_id: int,
        expense_id: int,
        operator_id: int = None,
        ip_address: str = None
    ) -> bool:
        """
        删除成本记录
        """
        expense = ExpenseRecordService.get_expense(db, user_id, expense_id)
        if not expense:
            return False
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='expense_delete',
            operator_id=operator_id or user_id,
            entity_type='expense_record',
            entity_id=expense.id,
            data={
                'category': expense.category,
                'amount': float(expense.amount),
                'expense_date': str(expense.expense_date)
            },
            ip_address=ip_address
        )
        
        db.delete(expense)
        db.commit()
        
        return True

    @staticmethod
    def get_summary(
        db: Session,
        user_id: int,
        start_date: date = None,
        end_date: date = None
    ) -> Dict:
        """
        获取成本汇总
        """
        query = db.query(ExpenseRecord).filter(ExpenseRecord.user_id == user_id)
        
        if start_date:
            query = query.filter(ExpenseRecord.expense_date >= start_date)
        if end_date:
            query = query.filter(ExpenseRecord.expense_date <= end_date)
        
        expenses = query.all()
        
        total_amount = Decimal('0')
        category_breakdown: Dict[str, Decimal] = {}
        behavior_breakdown: Dict[str, Decimal] = {}
        function_breakdown: Dict[str, Decimal] = {}
        
        for expense in expenses:
            total_amount += expense.amount
            
            if expense.category not in category_breakdown:
                category_breakdown[expense.category] = Decimal('0')
            category_breakdown[expense.category] += expense.amount
            
            if expense.cost_behavior:
                if expense.cost_behavior not in behavior_breakdown:
                    behavior_breakdown[expense.cost_behavior] = Decimal('0')
                behavior_breakdown[expense.cost_behavior] += expense.amount
            
            if expense.cost_function:
                if expense.cost_function not in function_breakdown:
                    function_breakdown[expense.cost_function] = Decimal('0')
                function_breakdown[expense.cost_function] += expense.amount
        
        return {
            'total_amount': total_amount,
            'category_breakdown': {k: float(v) for k, v in category_breakdown.items()},
            'behavior_breakdown': {k: float(v) for k, v in behavior_breakdown.items()},
            'function_breakdown': {k: float(v) for k, v in function_breakdown.items()}
        }

    @staticmethod
    def get_category_options() -> Dict:
        """
        获取成本分类选项
        """
        return {
            'categories': [{'value': c[0], 'label': c[1]} for c in EXPENSE_CATEGORIES],
            'cost_behaviors': [{'value': c[0], 'label': c[1]} for c in COST_BEHAVIORS],
            'cost_functions': [{'value': c[0], 'label': c[1]} for c in COST_FUNCTIONS]
        }
