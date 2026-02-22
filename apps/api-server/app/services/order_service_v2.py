"""
Dot-Store V2.2 订单服务
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.payment import Payment
from ..services.event_service import EventService


class OrderServiceV2:
    """
    订单服务类 - V2.2版本
    """

    @staticmethod
    def generate_order_no(db: Session, user_id: int) -> str:
        """
        生成订单编号
        格式：O + 日期(YYYYMMDD) + 4位序号
        """
        today = date.today()
        prefix = f"O{today.strftime('%Y%m%d')}"
        
        last_order = db.query(Order).filter(
            Order.order_no.like(f"{prefix}%")
        ).order_by(Order.order_no.desc()).first()
        
        if last_order:
            last_seq = int(last_order.order_no[-4:])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        
        return f"{prefix}{new_seq:04d}"

    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        order_type: str,
        amount: Decimal,
        payment_method: str = None,
        customer_account_id: int = None,
        category_id: int = None,
        tags: list = None,
        note: str = None,
        items: list = None,
        created_by: int = None,
        ip_address: str = None
    ) -> Order:
        """
        创建订单
        """
        order_no = OrderServiceV2.generate_order_no(db, user_id)
        
        order = Order(
            user_id=user_id,
            order_no=order_no,
            order_type=order_type,
            amount=amount,
            payment_method=payment_method,
            customer_account_id=customer_account_id,
            category_id=category_id,
            tags=tags,
            note=note,
            status='completed',
            created_by=created_by or user_id
        )
        
        db.add(order)
        db.flush()
        
        if items:
            for item_data in items:
                item = OrderItem(
                    order_id=order.id,
                    product_name=item_data.get('product_name'),
                    quantity=Decimal(str(item_data.get('quantity', 0))),
                    unit_price=Decimal(str(item_data.get('unit_price', 0))),
                    cost_price=Decimal(str(item_data.get('cost_price', 0))) if item_data.get('cost_price') else None,
                    amount=Decimal(str(item_data.get('quantity', 0))) * Decimal(str(item_data.get('unit_price', 0))),
                    note=item_data.get('note')
                )
                db.add(item)
        
        db.commit()
        db.refresh(order)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='order_created',
            operator_id=created_by or user_id,
            entity_type='order',
            entity_id=order.id,
            data={
                'order_no': order_no,
                'amount': float(amount),
                'order_type': order_type,
                'payment_method': payment_method
            },
            ip_address=ip_address
        )
        
        return order

    @staticmethod
    def get_orders(
        db: Session,
        user_id: int,
        start_date: date = None,
        end_date: date = None,
        order_type: str = None,
        status: str = None,
        is_deleted: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> tuple:
        """
        获取订单列表
        """
        query = db.query(Order).filter(Order.user_id == user_id)
        
        if not is_deleted:
            query = query.filter(Order.is_deleted == False)
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at < end_date)
        if order_type:
            query = query.filter(Order.order_type == order_type)
        if status:
            query = query.filter(Order.status == status)
        
        total = query.count()
        orders = query.order_by(Order.created_at.desc()) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .all()
        
        return orders, total

    @staticmethod
    def get_order(db: Session, user_id: int, order_id: int) -> Optional[Order]:
        """
        获取订单详情
        """
        return db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()

    @staticmethod
    def get_order_with_items(db: Session, user_id: int, order_id: int) -> Optional[Order]:
        """
        获取订单详情（含订单项）
        """
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
        
        if order:
            order.items = db.query(OrderItem).filter(
                OrderItem.order_id == order_id
            ).all()
        
        return order

    @staticmethod
    def update_order(
        db: Session,
        user_id: int,
        order_id: int,
        **kwargs
    ) -> Order:
        """
        更新订单
        """
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
        
        if not order:
            raise ValueError("订单不存在")
        
        for key, value in kwargs.items():
            if hasattr(order, key) and value is not None:
                setattr(order, key, value)
        
        db.commit()
        db.refresh(order)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='order_updated',
            operator_id=user_id,
            entity_type='order',
            entity_id=order.id,
            data={'order_no': order.order_no}
        )
        
        return order

    @staticmethod
    def void_order(
        db: Session,
        user_id: int,
        order_id: int,
        reason: str,
        voided_by: int = None,
        ip_address: str = None
    ) -> Order:
        """
        作废订单
        """
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
        
        if not order:
            raise ValueError("订单不存在")
        
        if order.is_deleted:
            raise ValueError("订单已作废")
        
        order.is_deleted = True
        order.status = 'voided'
        order.deleted_at = datetime.utcnow()
        order.deleted_by = voided_by or user_id
        
        db.commit()
        db.refresh(order)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='order_voided',
            operator_id=voided_by or user_id,
            entity_type='order',
            entity_id=order.id,
            data={
                'order_no': order.order_no,
                'reason': reason
            },
            ip_address=ip_address
        )
        
        return order

    @staticmethod
    def get_today_summary(db: Session, user_id: int) -> dict:
        """
        获取今日订单汇总
        """
        today = date.today()
        tomorrow = date(today.year, today.month, today.day + 1) if today.day < 28 else date(today.year, today.month + 1, 1) if today.month < 12 else date(today.year + 1, 1, 1)
        
        orders = db.query(Order).filter(
            Order.user_id == user_id,
            Order.created_at >= today,
            Order.created_at < tomorrow,
            Order.is_deleted == False
        ).all()
        
        total_orders = len(orders)
        total_amount = sum(float(o.amount) for o in orders)
        
        by_type = {}
        by_payment = {}
        
        for order in orders:
            if order.order_type not in by_type:
                by_type[order.order_type] = {'count': 0, 'amount': 0}
            by_type[order.order_type]['count'] += 1
            by_type[order.order_type]['amount'] += float(order.amount)
            
            if order.payment_method:
                if order.payment_method not in by_payment:
                    by_payment[order.payment_method] = {'count': 0, 'amount': 0}
                by_payment[order.payment_method]['count'] += 1
                by_payment[order.payment_method]['amount'] += float(order.amount)
        
        return {
            'total_orders': total_orders,
            'total_amount': total_amount,
            'by_type': by_type,
            'by_payment': by_payment
        }

    @staticmethod
    def add_order_item(
        db: Session,
        user_id: int,
        order_id: int,
        product_name: str,
        quantity: Decimal,
        unit_price: Decimal,
        cost_price: Decimal = None,
        note: str = None
    ) -> OrderItem:
        """
        添加订单项
        """
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
        
        if not order:
            raise ValueError("订单不存在")
        
        item = OrderItem(
            order_id=order_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
            cost_price=cost_price,
            amount=quantity * unit_price,
            note=note
        )
        
        db.add(item)
        db.commit()
        db.refresh(item)
        
        return item

    @staticmethod
    def get_order_items(db: Session, order_id: int) -> List[OrderItem]:
        """
        获取订单项列表
        """
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    @staticmethod
    def delete_order_item(db: Session, user_id: int, item_id: int) -> bool:
        """
        删除订单项
        """
        item = db.query(OrderItem).join(Order).filter(
            OrderItem.id == item_id,
            Order.user_id == user_id
        ).first()
        
        if not item:
            raise ValueError("订单项不存在")
        
        db.delete(item)
        db.commit()
        
        return True
