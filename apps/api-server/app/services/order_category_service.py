"""
Dot-Store V2.1 订单分类服务层
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.order import OrderCategory, Order
from app.schemas.order import OrderCategoryCreate, OrderCategoryUpdate


class OrderCategoryService:
    """
    订单分类服务类
    """

    def __init__(self, db: Session):
        """
        初始化订单分类服务
        """
        self.db = db

    def create_category(self, user_id: int, category_data: OrderCategoryCreate) -> OrderCategory:
        """
        创建订单分类
        
        Args:
            user_id: 用户ID
            category_data: 分类创建数据
            
        Returns:
            OrderCategory: 创建的分类对象
        """
        category = OrderCategory(
            user_id=user_id,
            name=category_data.name,
            description=category_data.description,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_category(self, category_id: int, user_id: int) -> Optional[OrderCategory]:
        """
        获取分类详情
        
        Args:
            category_id: 分类ID
            user_id: 用户ID
            
        Returns:
            OrderCategory: 分类对象，不存在则返回None
        """
        return self.db.query(OrderCategory).filter(
            and_(OrderCategory.id == category_id, OrderCategory.user_id == user_id)
        ).first()

    def list_categories(self, user_id: int) -> List[OrderCategory]:
        """
        获取分类列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[OrderCategory]: 分类列表
        """
        return self.db.query(OrderCategory).filter(
            OrderCategory.user_id == user_id
        ).order_by(OrderCategory.created_at.desc()).all()

    def update_category(self, category_id: int, user_id: int, category_data: OrderCategoryUpdate) -> Optional[OrderCategory]:
        """
        更新分类
        
        Args:
            category_id: 分类ID
            user_id: 用户ID
            category_data: 分类更新数据
            
        Returns:
            OrderCategory: 更新后的分类对象，不存在则返回None
        """
        category = self.get_category(category_id, user_id)
        if not category:
            return None

        update_data = category_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)

        category.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int, user_id: int) -> bool:
        """
        删除分类
        
        Args:
            category_id: 分类ID
            user_id: 用户ID
            
        Returns:
            bool: 删除成功返回True，分类不存在返回False
        """
        category = self.get_category(category_id, user_id)
        if not category:
            return False

        self.db.delete(category)
        self.db.commit()
        return True

    def get_category_usage_count(self, category_id: int, user_id: int) -> int:
        """
        获取分类使用次数
        
        Args:
            category_id: 分类ID
            user_id: 用户ID
            
        Returns:
            int: 使用次数
        """
        return self.db.query(Order).filter(
            and_(Order.category_id == category_id, Order.user_id == user_id, Order.is_deleted == False)
        ).count()
