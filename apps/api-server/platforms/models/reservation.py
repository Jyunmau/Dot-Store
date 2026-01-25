from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Reservation(Base):
    """预订模型 - Platform层核心模块，用于处理订台逻辑"""
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 预订基本信息
    reservation_no = Column(String(64), nullable=False, index=True, unique=True)  # 预订单号
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)  # 预订的酒台ID
    customer_id = Column(Integer, nullable=True, index=True)  # 预订人ID
    
    # 预订时间信息
    start_time = Column(TIMESTAMP(timezone=True), nullable=False, index=True)  # 预订开始时间
    end_time = Column(TIMESTAMP(timezone=True), nullable=False, index=True)  # 预订结束时间
    duration = Column(Integer, nullable=False)  # 预订时长（分钟）
    
    # 预订业务信息
    people_count = Column(Integer, nullable=False)  # 预订人数
    status = Column(String(32), default="pending", index=True)  # 预订状态：pending, confirmed, completed, cancelled, expired
    special_requests = Column(String(256), nullable=True)  # 特殊要求
    
    # 与Event模块的集成
    resource_event_id = Column(Integer, nullable=True, index=True)  # 关联的ResourceEvent ID
    
    # 支付信息
    deposit_amount = Column(Integer, nullable=True)  # 定金金额（分）
    deposit_status = Column(String(32), nullable=True)  # 定金状态：unpaid, paid, refunded
    payment_method = Column(String(32), nullable=True)  # 支付方式
    
    # 操作信息
    created_by = Column(Integer, nullable=True)  # 创建人ID
    confirmed_by = Column(Integer, nullable=True)  # 确认人ID
    confirmed_at = Column(TIMESTAMP(timezone=True), nullable=True)  # 确认时间
    cancelled_by = Column(Integer, nullable=True)  # 取消人ID
    cancelled_at = Column(TIMESTAMP(timezone=True), nullable=True)  # 取消时间
    cancellation_reason = Column(String(256), nullable=True)  # 取消原因
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Reservation(id={self.id}, shop_id={self.shop_id}, reservation_no={self.reservation_no}, table_id={self.table_id}, status={self.status})>"