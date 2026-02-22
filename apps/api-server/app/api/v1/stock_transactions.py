"""
Dot-Store V2.2 库存流水API路由
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.stock_transaction import (
    StockInRequest,
    StockOutRequest,
    StockAdjustRequest,
    StockTransactionResponse,
    StockTransactionListResponse,
    StockWarning,
    StockSummary,
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse,
    IngredientListResponse,
)
from app.services.stock_transaction_service import StockTransactionService
from app.models.user import User
from app.models.stock import Ingredient

router = APIRouter(prefix="/stock", tags=["库存管理"])


@router.get("/transactions", response_model=StockTransactionListResponse, summary="获取库存流水列表")
async def get_transactions(
    ingredient_id: Optional[int] = Query(None, description="食材ID"),
    transaction_type: Optional[str] = Query(None, description="交易类型"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存流水列表
    
    - 支持按食材筛选
    - 支持按交易类型筛选
    - 支持按日期范围筛选
    - 支持分页
    """
    transactions, total = StockTransactionService.get_transactions(
        db=db,
        user_id=current_user.id,
        ingredient_id=ingredient_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size
    )
    
    return StockTransactionListResponse(
        items=[StockTransactionResponse.model_validate(t) for t in transactions],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/transactions/{transaction_id}", response_model=StockTransactionResponse, summary="获取库存流水详情")
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存流水详情
    """
    transaction = StockTransactionService.get_transaction(db, current_user.id, transaction_id)
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="库存流水不存在"
        )
    
    return StockTransactionResponse.model_validate(transaction)


@router.post("/in", response_model=StockTransactionResponse, summary="入库操作")
async def stock_in(
    request: StockInRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    入库操作
    
    - 增加库存数量
    - 更新成本单价（加权平均）
    - 记录库存流水
    - 记录事件日志
    """
    try:
        transaction = StockTransactionService.stock_in(
            db=db,
            user_id=current_user.id,
            ingredient_id=request.ingredient_id,
            quantity=Decimal(str(request.quantity)),
            cost=Decimal(str(request.cost)) if request.cost else None,
            note=request.note,
            operator_id=current_user.id
        )
        return StockTransactionResponse.model_validate(transaction)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/out", response_model=StockTransactionResponse, summary="出库操作")
async def stock_out(
    request: StockOutRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    出库操作
    
    - 减少库存数量
    - 检查库存充足
    - 记录库存流水
    - 记录事件日志
    """
    try:
        transaction = StockTransactionService.stock_out(
            db=db,
            user_id=current_user.id,
            ingredient_id=request.ingredient_id,
            quantity=Decimal(str(request.quantity)),
            note=request.note,
            operator_id=current_user.id
        )
        return StockTransactionResponse.model_validate(transaction)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/adjust", response_model=StockTransactionResponse, summary="库存调整")
async def adjust_stock(
    request: StockAdjustRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    库存调整
    
    - 支持正数（增加）和负数（减少）
    - 记录库存流水
    - 记录事件日志
    """
    try:
        transaction = StockTransactionService.adjust_stock(
            db=db,
            user_id=current_user.id,
            ingredient_id=request.ingredient_id,
            quantity=Decimal(str(request.quantity)),
            note=request.note,
            operator_id=current_user.id
        )
        return StockTransactionResponse.model_validate(transaction)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/warnings", response_model=list[StockWarning], summary="获取库存预警")
async def get_stock_warnings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存预警列表
    
    - 低库存预警
    - 即将过期预警
    """
    warnings = StockTransactionService.get_stock_warnings(db, current_user.id)
    return [StockWarning(**w) for w in warnings]


@router.get("/summary", response_model=StockSummary, summary="获取库存汇总")
async def get_stock_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存汇总
    
    - 食材总数
    - 库存总价值
    - 低库存数量
    - 即将过期数量
    """
    summary = StockTransactionService.get_stock_summary(db, current_user.id)
    return StockSummary(**summary)


@router.get("/value", summary="获取库存总价值")
async def get_stock_value(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取库存总价值
    """
    value = StockTransactionService.get_total_stock_value(db, current_user.id)
    return {"total_value": float(value)}


@router.get("/ingredients", response_model=IngredientListResponse, summary="获取食材列表")
async def get_ingredients(
    category: Optional[str] = Query(None, description="分类"),
    status: Optional[str] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取食材列表
    """
    query = db.query(Ingredient).filter(Ingredient.user_id == current_user.id)
    
    if category:
        query = query.filter(Ingredient.category == category)
    if status:
        query = query.filter(Ingredient.status == status)
    
    total = query.count()
    ingredients = query.order_by(Ingredient.created_at.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()
    
    return IngredientListResponse(
        items=[IngredientResponse.model_validate(i) for i in ingredients],
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/ingredients", response_model=IngredientResponse, summary="创建食材")
async def create_ingredient(
    ingredient_data: IngredientCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建食材
    """
    ingredient = Ingredient(
        user_id=current_user.id,
        name=ingredient_data.name,
        unit=ingredient_data.unit,
        current_stock=ingredient_data.current_stock,
        min_stock=ingredient_data.min_stock,
        cost_per_unit=ingredient_data.cost_per_unit,
        category=ingredient_data.category,
        supplier=ingredient_data.supplier,
        expiry_date=ingredient_data.expiry_date,
        status='active'
    )
    
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    
    return IngredientResponse.model_validate(ingredient)


@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse, summary="获取食材详情")
async def get_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取食材详情
    """
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.user_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    return IngredientResponse.model_validate(ingredient)


@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse, summary="更新食材")
async def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新食材
    """
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.user_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    for key, value in ingredient_data.model_dump(exclude_unset=True).items():
        setattr(ingredient, key, value)
    
    db.commit()
    db.refresh(ingredient)
    
    return IngredientResponse.model_validate(ingredient)


@router.delete("/ingredients/{ingredient_id}", summary="删除食材")
async def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除食材（软删除）
    """
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.user_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="食材不存在"
        )
    
    ingredient.status = 'inactive'
    db.commit()
    
    return {"message": "食材删除成功"}
