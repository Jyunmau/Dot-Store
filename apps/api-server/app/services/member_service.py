"""
Dot-Store V2.1 会员服务层
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.member import Member, PointsRecord, PointsExchange
from app.schemas.member import (
    MemberCreate,
    MemberUpdate,
    PointsAddParams,
    PointsSubtractParams,
    PointsExchangeParams,
)


class MemberService:
    """
    会员服务类
    """

    def __init__(self, db: Session):
        """
        初始化会员服务
        """
        self.db = db

    def create_member(self, user_id: int, member_data: MemberCreate) -> Member:
        """
        创建会员

        Args:
            user_id: 用户ID
            member_data: 会员创建数据

        Returns:
            Member: 创建的会员对象
        """
        member = Member(
            user_id=user_id,
            name=member_data.name,
            phone=member_data.phone,
            level=member_data.level,
            points=0,
        )
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_member(self, member_id: int, user_id: int) -> Optional[Member]:
        """
        获取会员详情

        Args:
            member_id: 会员ID
            user_id: 用户ID

        Returns:
            Member: 会员对象，不存在则返回None
        """
        return self.db.query(Member).filter(
            and_(Member.id == member_id, Member.user_id == user_id)
        ).first()

    def list_members(self, user_id: int, page: int = 1, page_size: int = 10,
                     level: Optional[str] = None, keyword: Optional[str] = None) -> dict:
        """
        获取会员列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
            level: 会员等级筛选
            keyword: 关键词搜索（姓名或手机号）

        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(Member).filter(Member.user_id == user_id)

        if level:
            query = query.filter(Member.level == level)

        if keyword:
            query = query.filter(
                and_(
                    Member.name.contains(keyword) | Member.phone.contains(keyword)
                )
            )

        total = query.count()
        offset = (page - 1) * page_size

        members = query.order_by(Member.created_at.desc()).offset(offset).limit(page_size).all()

        return {
            "items": members,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def update_member(self, member_id: int, user_id: int, member_data: MemberUpdate) -> Optional[Member]:
        """
        更新会员

        Args:
            member_id: 会员ID
            user_id: 用户ID
            member_data: 会员更新数据

        Returns:
            Member: 更新后的会员对象，不存在则返回None
        """
        member = self.get_member(member_id, user_id)
        if not member:
            return None

        update_data = member_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(member, key, value)

        member.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(member)
        return member

    def delete_member(self, member_id: int, user_id: int) -> bool:
        """
        删除会员

        Args:
            member_id: 会员ID
            user_id: 用户ID

        Returns:
            bool: 删除成功返回True，会员不存在返回False
        """
        member = self.get_member(member_id, user_id)
        if not member:
            return False

        self.db.delete(member)
        self.db.commit()
        return True


class PointsService:
    """
    积分服务类
    """

    def __init__(self, db: Session):
        """
        初始化积分服务
        """
        self.db = db

    def add_points(self, user_id: int, params: PointsAddParams) -> PointsRecord:
        """
        增加会员积分

        Args:
            user_id: 用户ID
            params: 增加积分参数

        Returns:
            PointsRecord: 积分记录对象

        Raises:
            ValueError: 会员不存在
        """
        member = self.db.query(Member).filter(
            and_(Member.id == params.member_id, Member.user_id == user_id)
        ).first()

        if not member:
            raise ValueError("会员不存在")

        member.points += params.points
        member.updated_at = datetime.utcnow()

        record = PointsRecord(
            member_id=params.member_id,
            user_id=user_id,
            type="add",
            points=params.points,
            reason=params.reason,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def subtract_points(self, user_id: int, params: PointsSubtractParams) -> PointsRecord:
        """
        减少会员积分

        Args:
            user_id: 用户ID
            params: 减少积分参数

        Returns:
            PointsRecord: 积分记录对象

        Raises:
            ValueError: 会员不存在或积分不足
        """
        member = self.db.query(Member).filter(
            and_(Member.id == params.member_id, Member.user_id == user_id)
        ).first()

        if not member:
            raise ValueError("会员不存在")

        if member.points < params.points:
            raise ValueError("积分不足")

        member.points -= params.points
        member.updated_at = datetime.utcnow()

        record = PointsRecord(
            member_id=params.member_id,
            user_id=user_id,
            type="subtract",
            points=params.points,
            reason=params.reason,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_points_records(self, user_id: int, member_id: Optional[int] = None,
                           page: int = 1, page_size: int = 10) -> dict:
        """
        获取积分记录列表

        Args:
            user_id: 用户ID
            member_id: 会员ID（可选，不传则获取所有会员的记录）
            page: 页码
            page_size: 每页数量

        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(PointsRecord).filter(PointsRecord.user_id == user_id)

        if member_id:
            query = query.filter(PointsRecord.member_id == member_id)

        total = query.count()
        offset = (page - 1) * page_size

        records = query.order_by(PointsRecord.created_at.desc()).offset(offset).limit(page_size).all()

        members = self.db.query(Member).filter(Member.user_id == user_id).all()
        member_map = {m.id: m.name for m in members}

        items_with_name = []
        for record in records:
            record_dict = {
                "id": record.id,
                "member_id": record.member_id,
                "user_id": record.user_id,
                "type": record.type,
                "points": record.points,
                "reason": record.reason,
                "created_at": record.created_at,
                "member_name": member_map.get(record.member_id),
            }
            items_with_name.append(record_dict)

        return {
            "items": items_with_name,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def exchange_points(self, user_id: int, params: PointsExchangeParams) -> PointsExchange:
        """
        积分兑换

        Args:
            user_id: 用户ID
            params: 积分兑换参数

        Returns:
            PointsExchange: 积分兑换对象

        Raises:
            ValueError: 会员不存在或积分不足
        """
        member = self.db.query(Member).filter(
            and_(Member.id == params.member_id, Member.user_id == user_id)
        ).first()

        if not member:
            raise ValueError("会员不存在")

        if member.points < params.points:
            raise ValueError("积分不足")

        member.points -= params.points
        member.updated_at = datetime.utcnow()

        exchange = PointsExchange(
            member_id=params.member_id,
            user_id=user_id,
            points=params.points,
            amount=params.amount,
        )
        self.db.add(exchange)

        record = PointsRecord(
            member_id=params.member_id,
            user_id=user_id,
            type="subtract",
            points=params.points,
            reason=f"积分兑换，金额：{params.amount}元",
        )
        self.db.add(record)

        self.db.commit()
        self.db.refresh(exchange)
        return exchange

    def get_exchanges(self, user_id: int, page: int = 1, page_size: int = 10) -> dict:
        """
        获取积分兑换记录列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            dict: 包含items, total, page, page_size的字典
        """
        query = self.db.query(PointsExchange).filter(PointsExchange.user_id == user_id)

        total = query.count()
        offset = (page - 1) * page_size

        exchanges = query.order_by(PointsExchange.created_at.desc()).offset(offset).limit(page_size).all()

        members = self.db.query(Member).filter(Member.user_id == user_id).all()
        member_map = {m.id: m.name for m in members}

        items_with_name = []
        for exchange in exchanges:
            exchange_dict = {
                "id": exchange.id,
                "member_id": exchange.member_id,
                "user_id": exchange.user_id,
                "points": exchange.points,
                "amount": exchange.amount,
                "created_at": exchange.created_at,
                "member_name": member_map.get(exchange.member_id),
            }
            items_with_name.append(exchange_dict)

        return {
            "items": items_with_name,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
