"""
Dot-Store V2.1 库存服务层
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.stock import Ingredient, StockRecord
from app.schemas.stock import (
    IngredientCreate,
    IngredientUpdate,
    StockRecordCreate,
    StockWarningResponse,
    StockSummaryResponse,
)


class StockService:
    """
    库存服务类
    """

    def __init__(self, db: Session):
        """
        初始化库存服务
        """
        self.db = db

    def create_ingredient(self, user_id: int, data: IngredientCreate) -> Ingredient:
        """
        创建食材
        
        Args:
            user_id: 用户ID
            data: 食材创建数据
            
        Returns:
            Ingredient: 创建的食材对象
        """
        ingredient = Ingredient(
            user_id=user_id,
            name=data.name,
            unit=data.unit,
            current_stock=data.current_stock,
            warning_stock=data.warning_stock,
        )
        self.db.add(ingredient)
        self.db.commit()
        self.db.refresh(ingredient)
        return ingredient

    def get_ingredient(self, ingredient_id: int, user_id: int) -> Optional[Ingredient]:
        """
        获取食材详情
        
        Args:
            ingredient_id: 食材ID
            user_id: 用户ID
            
        Returns:
            Ingredient: 食材对象，不存在则返回None
        """
        return self.db.query(Ingredient).filter(
            and_(Ingredient.id == ingredient_id, Ingredient.user_id == user_id)
        ).first()

    def list_ingredients(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 100,
        name: Optional[str] = None
    ) -> dict:
        """
        获取食材列表
        
        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
            name: 食材名称筛选
            
        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(Ingredient).filter(Ingredient.user_id == user_id)
        
        if name:
            query = query.filter(Ingredient.name.ilike(f"%{name}%"))
        
        total = query.count()
        offset = (page - 1) * page_size
        
        ingredients = query.order_by(Ingredient.created_at.desc()).offset(offset).limit(page_size).all()
        
        return {
            "items": ingredients,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def update_ingredient(
        self,
        ingredient_id: int,
        user_id: int,
        data: IngredientUpdate
    ) -> Optional[Ingredient]:
        """
        更新食材
        
        Args:
            ingredient_id: 食材ID
            user_id: 用户ID
            data: 食材更新数据
            
        Returns:
            Ingredient: 更新后的食材对象，不存在则返回None
        """
        ingredient = self.get_ingredient(ingredient_id, user_id)
        if not ingredient:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ingredient, key, value)
        
        ingredient.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(ingredient)
        return ingredient

    def delete_ingredient(self, ingredient_id: int, user_id: int) -> bool:
        """
        删除食材
        
        Args:
            ingredient_id: 食材ID
            user_id: 用户ID
            
        Returns:
            bool: 删除成功返回True，食材不存在返回False
        """
        ingredient = self.get_ingredient(ingredient_id, user_id)
        if not ingredient:
            return False
        
        self.db.delete(ingredient)
        self.db.commit()
        return True

    def record_stock_in(
        self,
        user_id: int,
        data: StockRecordCreate
    ) -> Optional[StockRecord]:
        """
        记录库存入库
        
        Args:
            user_id: 用户ID
            data: 库存记录数据
            
        Returns:
            StockRecord: 创建的库存记录对象
        """
        ingredient = self.get_ingredient(data.ingredient_id, user_id)
        if not ingredient:
            return None
        
        record = StockRecord(
            ingredient_id=data.ingredient_id,
            user_id=user_id,
            type="in",
            quantity=data.quantity,
            note=data.note,
        )
        self.db.add(record)
        
        ingredient.current_stock += data.quantity
        ingredient.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(record)
        return record

    def record_stock_out(
        self,
        user_id: int,
        data: StockRecordCreate
    ) -> Optional[StockRecord]:
        """
        记录库存出库
        
        Args:
            user_id: 用户ID
            data: 库存记录数据
            
        Returns:
            StockRecord: 创建的库存记录对象
        """
        ingredient = self.get_ingredient(data.ingredient_id, user_id)
        if not ingredient:
            return None
        
        if ingredient.current_stock < data.quantity:
            return None
        
        record = StockRecord(
            ingredient_id=data.ingredient_id,
            user_id=user_id,
            type="out",
            quantity=data.quantity,
            note=data.note,
        )
        self.db.add(record)
        
        ingredient.current_stock -= data.quantity
        ingredient.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_stock_records(
        self,
        user_id: int,
        ingredient_id: Optional[int] = None,
        record_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """
        获取库存记录列表
        
        Args:
            user_id: 用户ID
            ingredient_id: 食材ID筛选
            record_type: 记录类型筛选
            page: 页码
            page_size: 每页数量
            
        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(StockRecord).filter(StockRecord.user_id == user_id)
        
        if ingredient_id:
            query = query.filter(StockRecord.ingredient_id == ingredient_id)
        
        if record_type:
            query = query.filter(StockRecord.type == record_type)
        
        total = query.count()
        offset = (page - 1) * page_size
        
        records = query.order_by(StockRecord.created_at.desc()).offset(offset).limit(page_size).all()
        
        result_records = []
        for record in records:
            ingredient = self.db.query(Ingredient).filter(Ingredient.id == record.ingredient_id).first()
            record_dict = {
                "id": record.id,
                "ingredient_id": record.ingredient_id,
                "user_id": record.user_id,
                "type": record.type,
                "quantity": record.quantity,
                "note": record.note,
                "created_at": record.created_at,
                "ingredient_name": ingredient.name if ingredient else None,
                "ingredient_unit": ingredient.unit if ingredient else None,
            }
            result_records.append(record_dict)
        
        return {
            "items": result_records,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def get_stock_warnings(self, user_id: int) -> List[StockWarningResponse]:
        """
        获取库存预警列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[StockWarningResponse]: 库存预警列表
        """
        ingredients = self.db.query(Ingredient).filter(
            and_(
                Ingredient.user_id == user_id,
                Ingredient.current_stock < Ingredient.warning_stock
            )
        ).all()
        
        warnings = []
        for ingredient in ingredients:
            deficit = ingredient.warning_stock - ingredient.current_stock
            warning = StockWarningResponse(
                ingredient_id=ingredient.id,
                name=ingredient.name,
                unit=ingredient.unit,
                current_stock=ingredient.current_stock,
                warning_stock=ingredient.warning_stock,
                deficit=deficit,
            )
            warnings.append(warning)
        
        return warnings

    def get_stock_summary(self, user_id: int) -> StockSummaryResponse:
        """
        获取库存统计
        
        Args:
            user_id: 用户ID
            
        Returns:
            StockSummaryResponse: 库存统计信息
        """
        total_ingredients = self.db.query(Ingredient).filter(
            Ingredient.user_id == user_id
        ).count()
        
        low_stock_count = self.db.query(Ingredient).filter(
            and_(
                Ingredient.user_id == user_id,
                Ingredient.current_stock < Ingredient.warning_stock
            )
        ).count()
        
        return StockSummaryResponse(
            total_ingredients=total_ingredients,
            low_stock_count=low_stock_count,
            total_value=Decimal("0"),
        )
