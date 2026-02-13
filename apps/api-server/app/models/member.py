"""
Dot-Store V2.1 会员数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from ..core.database import Base


class Member(Base):
    """
    会员模型
    """
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(64), nullable=False)
    phone = Column(String(32), nullable=False, index=True)
    level = Column(String(32), nullable=False, default="normal", index=True)
    points = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Member(id={self.id}, name={self.name}, phone={self.phone}, level={self.level}, points={self.points})>"


class PointsRecord(Base):
    """
    积分记录模型
    """
    __tablename__ = "points_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    type = Column(String(32), nullable=False, index=True)
    points = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<PointsRecord(id={self.id}, member_id={self.member_id}, type={self.type}, points={self.points})>"


class PointsExchange(Base):
    """
    积分兑换模型
    """
    __tablename__ = "points_exchanges"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    points = Column(Integer, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<PointsExchange(id={self.id}, member_id={self.member_id}, points={self.points}, amount={self.amount})>"
