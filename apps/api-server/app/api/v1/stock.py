"""
Dot-Store V2.1 库存API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.stock import (
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse,
    IngredientListResponse,
    StockRecordCreate,
    StockRecordResponse,
    StockRecordListResponse,
    StockWarningResponse,
    StockSummaryResponse,
)
from app.services.stock_service import StockService
from app.models.user import User

router = APIRouter(prefix="/stock", tags=["库存管理"])


@router.post("/ingredients", response_model=IngredientResponse, summary="创建食材")
async def create_ingredient(
    data: IngredientCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建食材接口
    
    - 名称：必填，最长64字符
    - 单位：必填，最长16字符
    - 当前库存：默认0
    - 预警值：默认0
    """
    stock_service = StockService(db)
    ingredient = stock_service.create_ingredient(current_user.id, data)
    return IngredientResponse.model_validate(ingredient)


@router.get("/ingredients", response_model=IngredientListResponse, summary="获取食材列表")
async def list_ingredients(
    name: Optional[str] = Query(None, description="食材名称筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取食材列表接口
    
    - 支持按名称筛选
    - 支持分页
    """
    stock_service = StockService(db)
    result = stock_service.list_ingredients(current_user.id, page, page_size, name)
    
    return IngredientListResponse(
        items=[IngredientResponse.model_validate(ing) for ing in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse, summary="获取食材详情")
async def get_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取食材详情接口
    """
    stock_service = StockService(db)
    ingredient = stock_service.get_ingredient(ingredient_id, current_user.id)
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    return IngredientResponse.model_validate(ingredient)


@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse, summary="更新食材")
async def update_ingredient(
    ingredient_id: int,
    data: IngredientUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新食材接口
    
    - 支持更新名称、单位、当前库存、预警值
    """
    stock_service = StockService(db)
    ingredient = stock_service.update_ingredient(ingredient_id, current_user.id, data)
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    return IngredientResponse.model_validate(ingredient)


@router.delete("/ingredients/{ingredient_id}", summary="删除食材")
async def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除食材接口
    
    - 删除食材会同时删除相关的库存记录
    """
    stock_service = StockService(db)
    success = stock_service.delete_ingredient(ingredient_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    return {"message": "食材删除成功"}


@router.post("/records/in", response_model=StockRecordResponse, summary="记录库存入库")
async def record_stock_in(
    data: StockRecordCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    记录库存入库接口
    
    - 数量必须大于0
    - 入库后自动更新食材当前库存
    """
    stock_service = StockService(db)
    record = stock_service.record_stock_in(current_user.id, data)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    ingredient = stock_service.get_ingredient(data.ingredient_id, current_user.id)
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
    return StockRecordResponse.model_validate(record_dict)


@router.post("/records/out", response_model=StockRecordResponse, summary="记录库存出库")
async def record_stock_out(
    data: StockRecordCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    记录库存出库接口
    
    - 数量必须大于0
    - 出库数量不能超过当前库存
    - 出库后自动更新食材当前库存
    """
    stock_service = StockService(db)
    record = stock_service.record_stock_out(current_user.id, data)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="食材不存在或库存不足"
        )
    
    ingredient = stock_service.get_ingredient(data.ingredient_id, current_user.id)
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
    return StockRecordResponse.model_validate(record_dict)


@router.get("/records", response_model=StockRecordListResponse, summary="获取库存记录列表")
async def list_stock_records(
    ingredient_id: Optional[int] = Query(None, description="食材ID筛选"),
    type: Optional[str] = Query(None, description="类型筛选：in-入库，out-出库"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存记录列表接口
    
    - 支持按食材筛选
    - 支持按类型筛选
    - 支持分页
    """
    stock_service = StockService(db)
    result = stock_service.list_stock_records(
        current_user.id, ingredient_id, type, page, page_size
    )
    
    return StockRecordListResponse(
        items=[StockRecordResponse.model_validate(rec) for rec in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/warnings", response_model=list[StockWarningResponse], summary="获取库存预警列表")
async def get_stock_warnings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存预警列表接口
    
    - 返回当前库存低于预警值的食材列表
    """
    stock_service = StockService(db)
    warnings = stock_service.get_stock_warnings(current_user.id)
    return warnings


@router.get("/summary", response_model=StockSummaryResponse, summary="获取库存统计")
async def get_stock_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存统计接口
    
    - 返回食材总数、库存预警数量等信息
    """
    stock_service = StockService(db)
    summary = stock_service.get_stock_summary(current_user.id)
    return summary
