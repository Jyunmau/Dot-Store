"""
Dot-Store V2.1 会员API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.schemas.member import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
    MemberListResponse,
    PointsAddParams,
    PointsSubtractParams,
    PointsRecordResponse,
    PointsRecordListResponse,
    PointsExchangeParams,
    PointsExchangeResponse,
    PointsExchangeListResponse,
)
from app.services.member_service import MemberService, PointsService
from app.models.user import User

router = APIRouter(prefix="/members", tags=["会员管理"])


@router.post("", response_model=MemberResponse, summary="创建会员")
async def create_member(
    member_data: MemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建会员接口

    - 会员姓名和手机号为必填项
    - 会员等级默认为普通会员(normal)
    """
    member_service = MemberService(db)
    member = member_service.create_member(current_user.id, member_data)
    return MemberResponse.model_validate(member)


@router.get("", response_model=MemberListResponse, summary="获取会员列表")
async def list_members(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    level: Optional[str] = Query(None, description="会员等级筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索（姓名或手机号）"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取会员列表接口

    - 支持按会员等级筛选
    - 支持按姓名或手机号搜索
    - 支持分页
    """
    member_service = MemberService(db)
    result = member_service.list_members(
        current_user.id, page, page_size, level, keyword
    )

    return MemberListResponse(
        items=[MemberResponse.model_validate(member) for member in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.post("/points/add", response_model=PointsRecordResponse, summary="增加积分")
async def add_points(
    params: PointsAddParams,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    增加会员积分接口

    - 积分数量必须大于0
    - 原因为必填项
    """
    points_service = PointsService(db)
    try:
        record = points_service.add_points(current_user.id, params)
        member_service = MemberService(db)
        member = member_service.get_member(params.member_id, current_user.id)
        response = PointsRecordResponse.model_validate(record)
        response.member_name = member.name if member else None
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/points/subtract", response_model=PointsRecordResponse, summary="减少积分")
async def subtract_points(
    params: PointsSubtractParams,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    减少会员积分接口

    - 积分数量必须大于0
    - 原因为必填项
    - 积分不足时返回错误
    """
    points_service = PointsService(db)
    try:
        record = points_service.subtract_points(current_user.id, params)
        member_service = MemberService(db)
        member = member_service.get_member(params.member_id, current_user.id)
        response = PointsRecordResponse.model_validate(record)
        response.member_name = member.name if member else None
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/points/{member_id}", response_model=PointsRecordListResponse, summary="获取会员积分记录")
async def get_points_records(
    member_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取会员积分记录接口

    - 支持分页
    """
    points_service = PointsService(db)
    result = points_service.get_points_records(current_user.id, member_id, page, page_size)

    return PointsRecordListResponse(
        items=[PointsRecordResponse.model_validate(record) for record in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.post("/exchange", response_model=PointsExchangeResponse, summary="积分兑换")
async def exchange_points(
    params: PointsExchangeParams,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    积分兑换接口

    - 兑换积分数量必须大于0
    - 兑换金额必须大于0
    - 积分不足时返回错误
    """
    points_service = PointsService(db)
    try:
        exchange = points_service.exchange_points(current_user.id, params)
        member_service = MemberService(db)
        member = member_service.get_member(params.member_id, current_user.id)
        response = PointsExchangeResponse.model_validate(exchange)
        response.member_name = member.name if member else None
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/exchanges", response_model=PointsExchangeListResponse, summary="获取积分兑换记录")
async def get_exchanges(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取积分兑换记录接口

    - 支持分页
    """
    points_service = PointsService(db)
    result = points_service.get_exchanges(current_user.id, page, page_size)

    return PointsExchangeListResponse(
        items=[PointsExchangeResponse.model_validate(exchange) for exchange in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/{member_id}", response_model=MemberResponse, summary="获取会员详情")
async def get_member(
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取会员详情接口
    """
    member_service = MemberService(db)
    member = member_service.get_member(member_id, current_user.id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会员不存在"
        )

    return MemberResponse.model_validate(member)


@router.put("/{member_id}", response_model=MemberResponse, summary="更新会员")
async def update_member(
    member_id: int,
    member_data: MemberUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新会员接口

    - 支持更新姓名、手机号、会员等级
    """
    member_service = MemberService(db)
    member = member_service.update_member(member_id, current_user.id, member_data)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会员不存在"
        )

    return MemberResponse.model_validate(member)


@router.delete("/{member_id}", summary="删除会员")
async def delete_member(
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    删除会员接口

    - 删除会员将同时删除相关的积分记录和兑换记录
    """
    member_service = MemberService(db)
    success = member_service.delete_member(member_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会员不存在"
        )

    return {"message": "会员删除成功"}
