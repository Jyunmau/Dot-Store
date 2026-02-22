"""
Dot-Store V2.2 库存流水服务
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.stock import Ingredient
from ..models.stock_transaction import StockTransaction
from ..services.event_service import EventService


class StockTransactionType:
    """库存交易类型"""
    PURCHASE = 'purchase'
    CONSUME = 'consume'
    ADJUST_ADD = 'adjust_add'
    ADJUST_SUB = 'adjust_sub'
    RETURN = 'return'
    TRANSFER_IN = 'transfer_in'
    TRANSFER_OUT = 'transfer_out'


class StockTransactionService:
    """
    库存流水服务类
    """

    @staticmethod
    def generate_transaction_no(prefix: str = 'T') -> str:
        """
        生成交易编号
        格式：前缀 + 时间戳 + 随机数
        """
        import random
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_num = random.randint(1000, 9999)
        return f"{prefix}{timestamp}{random_num}"

    @staticmethod
    def stock_in(
        db: Session,
        user_id: int,
        ingredient_id: int,
        quantity: Decimal,
        cost: Decimal = None,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> StockTransaction:
        """
        入库操作
        """
        ingredient = db.query(Ingredient).filter(
            Ingredient.id == ingredient_id,
            Ingredient.user_id == user_id
        ).with_for_update().first()
        
        if not ingredient:
            raise ValueError("食材不存在")
        
        stock_before = ingredient.current_stock
        ingredient.current_stock += quantity
        
        if cost and cost > 0:
            old_total = stock_before * (ingredient.cost_per_unit or Decimal(0))
            new_total = quantity * cost
            total_quantity = stock_before + quantity
            if total_quantity > 0:
                ingredient.cost_per_unit = (old_total + new_total) / total_quantity
        
        transaction = StockTransaction(
            user_id=user_id,
            ingredient_id=ingredient_id,
            transaction_no=StockTransactionService.generate_transaction_no('I'),
            transaction_type=StockTransactionType.PURCHASE,
            quantity=quantity,
            stock_before=stock_before,
            stock_after=ingredient.current_stock,
            unit_cost=cost,
            total_cost=quantity * cost if cost else None,
            note=note,
            operator_id=operator_id or user_id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='stock_in',
            operator_id=operator_id or user_id,
            entity_type='ingredient',
            entity_id=ingredient_id,
            data={
                'quantity': float(quantity),
                'cost': float(cost) if cost else None,
                'stock_before': float(stock_before),
                'stock_after': float(ingredient.current_stock)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def stock_out(
        db: Session,
        user_id: int,
        ingredient_id: int,
        quantity: Decimal,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> StockTransaction:
        """
        出库操作
        """
        ingredient = db.query(Ingredient).filter(
            Ingredient.id == ingredient_id,
            Ingredient.user_id == user_id
        ).with_for_update().first()
        
        if not ingredient:
            raise ValueError("食材不存在")
        
        if ingredient.current_stock < quantity:
            raise ValueError(f"库存不足: 当前{ingredient.current_stock}, 需要{quantity}")
        
        stock_before = ingredient.current_stock
        ingredient.current_stock -= quantity
        
        transaction = StockTransaction(
            user_id=user_id,
            ingredient_id=ingredient_id,
            transaction_no=StockTransactionService.generate_transaction_no('O'),
            transaction_type=StockTransactionType.CONSUME,
            quantity=quantity,
            stock_before=stock_before,
            stock_after=ingredient.current_stock,
            unit_cost=ingredient.cost_per_unit,
            total_cost=quantity * (ingredient.cost_per_unit or Decimal(0)),
            note=note,
            operator_id=operator_id or user_id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='stock_out',
            operator_id=operator_id or user_id,
            entity_type='ingredient',
            entity_id=ingredient_id,
            data={
                'quantity': float(quantity),
                'stock_before': float(stock_before),
                'stock_after': float(ingredient.current_stock)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def adjust_stock(
        db: Session,
        user_id: int,
        ingredient_id: int,
        quantity: Decimal,
        note: str = None,
        operator_id: int = None,
        ip_address: str = None
    ) -> StockTransaction:
        """
        库存调整
        """
        ingredient = db.query(Ingredient).filter(
            Ingredient.id == ingredient_id,
            Ingredient.user_id == user_id
        ).with_for_update().first()
        
        if not ingredient:
            raise ValueError("食材不存在")
        
        stock_before = ingredient.current_stock
        ingredient.current_stock += quantity
        
        transaction_type = StockTransactionType.ADJUST_ADD if quantity > 0 else StockTransactionType.ADJUST_SUB
        
        transaction = StockTransaction(
            user_id=user_id,
            ingredient_id=ingredient_id,
            transaction_no=StockTransactionService.generate_transaction_no('A'),
            transaction_type=transaction_type,
            quantity=abs(quantity),
            stock_before=stock_before,
            stock_after=ingredient.current_stock,
            unit_cost=ingredient.cost_per_unit,
            total_cost=abs(quantity) * (ingredient.cost_per_unit or Decimal(0)),
            note=note,
            operator_id=operator_id or user_id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='stock_adjust',
            operator_id=operator_id or user_id,
            entity_type='ingredient',
            entity_id=ingredient_id,
            data={
                'quantity': float(quantity),
                'stock_before': float(stock_before),
                'stock_after': float(ingredient.current_stock)
            },
            ip_address=ip_address
        )
        
        return transaction

    @staticmethod
    def get_transactions(
        db: Session,
        user_id: int,
        ingredient_id: int = None,
        transaction_type: str = None,
        start_date: date = None,
        end_date: date = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple:
        """
        获取库存流水列表
        """
        query = db.query(StockTransaction).filter(StockTransaction.user_id == user_id)
        
        if ingredient_id:
            query = query.filter(StockTransaction.ingredient_id == ingredient_id)
        if transaction_type:
            query = query.filter(StockTransaction.transaction_type == transaction_type)
        if start_date:
            query = query.filter(StockTransaction.created_at >= start_date)
        if end_date:
            query = query.filter(StockTransaction.created_at < end_date)
        
        total = query.count()
        transactions = query.order_by(StockTransaction.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return transactions, total

    @staticmethod
    def get_transaction(db: Session, user_id: int, transaction_id: int) -> Optional[StockTransaction]:
        """
        获取库存流水详情
        """
        return db.query(StockTransaction).filter(
            StockTransaction.id == transaction_id,
            StockTransaction.user_id == user_id
        ).first()

    @staticmethod
    def get_stock_warnings(db: Session, user_id: int) -> List[dict]:
        """
        获取库存预警列表
        """
        warnings = []
        
        low_stock = db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active',
            Ingredient.current_stock <= Ingredient.min_stock,
            Ingredient.min_stock > 0
        ).all()
        
        for item in low_stock:
            warnings.append({
                'ingredient_id': item.id,
                'ingredient_name': item.name,
                'current_stock': float(item.current_stock),
                'min_stock': float(item.min_stock),
                'unit': item.unit,
                'warning_type': 'low_stock',
                'message': f"{item.name}库存不足，当前{item.current_stock}{item.unit}，最低{item.min_stock}{item.unit}"
            })
        
        from datetime import timedelta
        today = date.today()
        expiring = db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active',
            Ingredient.expiry_date.isnot(None),
            Ingredient.expiry_date <= today + timedelta(days=7),
            Ingredient.expiry_date >= today
        ).all()
        
        for item in expiring:
            warnings.append({
                'ingredient_id': item.id,
                'ingredient_name': item.name,
                'current_stock': float(item.current_stock),
                'expiry_date': str(item.expiry_date),
                'unit': item.unit,
                'warning_type': 'expiry',
                'message': f"{item.name}即将过期，过期日期{item.expiry_date}"
            })
        
        return warnings

    @staticmethod
    def get_total_stock_value(db: Session, user_id: int) -> Decimal:
        """
        计算库存总价值
        """
        from sqlalchemy import func
        
        result = db.query(
            func.sum(Ingredient.current_stock * Ingredient.cost_per_unit)
        ).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active'
        ).scalar()
        
        return result or Decimal(0)

    @staticmethod
    def get_stock_summary(db: Session, user_id: int) -> dict:
        """
        获取库存汇总
        """
        from sqlalchemy import func
        
        total_ingredients = db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active'
        ).count()
        
        total_value = StockTransactionService.get_total_stock_value(db, user_id)
        
        low_stock_count = db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active',
            Ingredient.current_stock <= Ingredient.min_stock,
            Ingredient.min_stock > 0
        ).count()
        
        from datetime import timedelta
        today = date.today()
        expiring_count = db.query(Ingredient).filter(
            Ingredient.user_id == user_id,
            Ingredient.status == 'active',
            Ingredient.expiry_date.isnot(None),
            Ingredient.expiry_date <= today + timedelta(days=7),
            Ingredient.expiry_date >= today
        ).count()
        
        return {
            'total_ingredients': total_ingredients,
            'total_value': float(total_value),
            'low_stock_count': low_stock_count,
            'expiring_count': expiring_count
        }
