"""
Dot-Store V2.1 收支分类服务层
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.transaction import TransactionCategory
from app.schemas.transaction import (
    TransactionCategoryCreate,
    TransactionCategoryUpdate,
)


class TransactionCategoryService:
    """
    收支分类服务类
    """

    def __init__(self, db: Session):
        """
        初始化收支分类服务
        """
        self.db = db

    def create_category(
        self, user_id: int, category_data: TransactionCategoryCreate
    ) -> TransactionCategory:
        """
        创建收支分类
        
        Args:
            user_id: 用户ID
            category_data: 分类创建数据
            
        Returns:
            TransactionCategory: 创建的分类对象
        """
        category = TransactionCategory(
            user_id=user_id,
            name=category_data.name,
            type=category_data.type,
            description=category_data.description,
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_category(
        self, category_id: int, user_id: int
    ) -> Optional[TransactionCategory]:
        """
        获取收支分类详情
        
        Args:
            category_id: 分类ID
            user_id: 用户ID
            
        Returns:
            TransactionCategory: 分类对象，不存在则返回None
        """
        return self.db.query(TransactionCategory).filter(
            and_(
                TransactionCategory.id == category_id,
                TransactionCategory.user_id == user_id,
            )
        ).first()

    def list_categories(
        self, user_id: int, type: Optional[str] = None
    ) -> List[TransactionCategory]:
        """
        获取收支分类列表
        
        Args:
            user_id: 用户ID
            type: 类型筛选（income/expense）
            
        Returns:
            List[TransactionCategory]: 分类列表
        """
        query = self.db.query(TransactionCategory).filter(
            TransactionCategory.user_id == user_id
        )

        if type:
            query = query.filter(TransactionCategory.type == type)

        return query.order_by(TransactionCategory.created_at.desc()).all()

    def update_category(
        self,
        category_id: int,
        user_id: int,
        category_data: TransactionCategoryUpdate,
    ) -> Optional[TransactionCategory]:
        """
        更新收支分类
        
        Args:
            category_id: 分类ID
            user_id: 用户ID
            category_data: 分类更新数据
            
        Returns:
            TransactionCategory: 更新后的分类对象，不存在则返回None
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
        删除收支分类
        
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

    def get_category_by_name(
        self, user_id: int, name: str, type: str
    ) -> Optional[TransactionCategory]:
        """
        根据名称获取分类
        
        Args:
            user_id: 用户ID
            name: 分类名称
            type: 分类类型
            
        Returns:
            TransactionCategory: 分类对象，不存在则返回None
        """
        return self.db.query(TransactionCategory).filter(
            and_(
                TransactionCategory.user_id == user_id,
                TransactionCategory.name == name,
                TransactionCategory.type == type,
            )
        ).first()

    def get_or_create_category(
        self, user_id: int, name: str, type: str, description: Optional[str] = None
    ) -> TransactionCategory:
        """
        获取或创建分类
        
        Args:
            user_id: 用户ID
            name: 分类名称
            type: 分类类型
            description: 分类描述
            
        Returns:
            TransactionCategory: 分类对象
        """
        category = self.get_category_by_name(user_id, name, type)
        if category:
            return category

        category_data = TransactionCategoryCreate(
            name=name, type=type, description=description
        )
        return self.create_category(user_id, category_data)
