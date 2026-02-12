"""
Dot-Store V2.1 订单服务层
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.order import Order, OrderCategory
from app.schemas.order import OrderCreate, OrderUpdate, OrderFilters


class OrderService:
    """
    订单服务类
    """

    def __init__(self, db: Session):
        """
        初始化订单服务
        """
        self.db = db

    def create_order(self, user_id: int, order_data: OrderCreate, created_by: int) -> Order:
        """
        创建订单
        
        Args:
            user_id: 用户ID
            order_data: 订单创建数据
            created_by: 创建人ID
            
        Returns:
            Order: 创建的订单对象
        """
        order = Order(
            user_id=user_id,
            amount=order_data.amount,
            order_type=order_data.order_type,
            category_id=order_data.category_id,
            tags=order_data.tags,
            order_metadata=order_data.order_metadata,
            status="recorded",
            created_by=created_by,
            is_deleted=False,
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: int, user_id: int) -> Optional[Order]:
        """
        获取订单详情
        
        Args:
            order_id: 订单ID
            user_id: 用户ID
            
        Returns:
            Order: 订单对象，不存在则返回None
        """
        return self.db.query(Order).filter(
            and_(Order.id == order_id, Order.user_id == user_id)
        ).first()

    def list_orders(self, user_id: int, filters: Optional[OrderFilters] = None) -> dict:
        """
        获取订单列表
        
        Args:
            user_id: 用户ID
            filters: 筛选条件
            
        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(Order).filter(
            and_(Order.user_id == user_id, Order.is_deleted == False)
        )

        if filters:
            if filters.start_date:
                query = query.filter(Order.created_at >= filters.start_date)
            if filters.end_date:
                query = query.filter(Order.created_at <= filters.end_date)
            if filters.order_type:
                query = query.filter(Order.order_type == filters.order_type)
            if filters.category_id:
                query = query.filter(Order.category_id == filters.category_id)
            if filters.status:
                query = query.filter(Order.status == filters.status)
            if filters.tags:
                query = query.filter(Order.tags.contains(filters.tags))

        total = query.count()

        page = filters.page if filters else 1
        page_size = filters.page_size if filters else 10
        offset = (page - 1) * page_size

        orders = query.order_by(Order.created_at.desc()).offset(offset).limit(page_size).all()

        return {
            "items": orders,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def update_order(self, order_id: int, user_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """
        更新订单
        
        Args:
            order_id: 订单ID
            user_id: 用户ID
            order_data: 订单更新数据
            
        Returns:
            Order: 更新后的订单对象，不存在则返回None
        """
        order = self.get_order(order_id, user_id)
        if not order:
            return None

        update_data = order_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order, key, value)

        order.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order_id: int, user_id: int) -> bool:
        """
        删除订单（软删除）
        
        Args:
            order_id: 订单ID
            user_id: 用户ID
            
        Returns:
            bool: 删除成功返回True，订单不存在返回False
        """
        order = self.get_order(order_id, user_id)
        if not order:
            return False

        order.is_deleted = True
        order.deleted_at = datetime.utcnow()
        self.db.commit()
        return True

    def restore_order(self, order_id: int, user_id: int) -> Optional[Order]:
        """
        恢复订单
        
        Args:
            order_id: 订单ID
            user_id: 用户ID
            
        Returns:
            Order: 恢复后的订单对象，不存在则返回None
        """
        order = self.db.query(Order).filter(
            and_(Order.id == order_id, Order.user_id == user_id, Order.is_deleted == True)
        ).first()
        if not order:
            return None

        order.is_deleted = False
        order.deleted_at = None
        order.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_deleted_orders(self, user_id: int, page: int = 1, page_size: int = 10) -> dict:
        """
        获取回收站订单列表
        
        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
            
        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(Order).filter(
            and_(Order.user_id == user_id, Order.is_deleted == True)
        )

        total = query.count()
        offset = (page - 1) * page_size

        orders = query.order_by(Order.deleted_at.desc()).offset(offset).limit(page_size).all()

        return {
            "items": orders,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def get_order_types(self, user_id: int) -> List[str]:
        """
        获取用户所有订单类型
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[str]: 订单类型列表
        """
        result = self.db.query(Order.order_type).filter(
            and_(Order.user_id == user_id, Order.is_deleted == False)
        ).distinct().all()
        return [r[0] for r in result]

    def get_order_tags(self, user_id: int) -> List[str]:
        """
        获取用户所有订单标签
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[str]: 标签列表
        """
        orders = self.db.query(Order.tags).filter(
            and_(Order.user_id == user_id, Order.is_deleted == False, Order.tags != None)
        ).all()
        
        tags_set = set()
        for order_tags in orders:
            if order_tags[0]:
                for tag in order_tags[0]:
                    tags_set.add(tag)
        
        return list(tags_set)
