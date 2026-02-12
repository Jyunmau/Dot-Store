from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Order(Base):
    """订单模型 - Platform层核心模块，用于餐饮/酒吧行业的订单管理"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    # 基础订单状态流转：recorded → confirmed → paid → completed → cancelled
    status = Column(String(32), default="recorded")
    amount_estimate = Column(Integer, default=0, nullable=False)  # 使用整数存储分，默认值0
    amount_actual = Column(Integer, nullable=True)  # 实际支付金额，使用整数存储分
    currency = Column(String(16), default="CNY")  # 货币类型
    tags = Column(JSON)  # 订单标签
    metadata_ = Column(JSON, name="metadata")  # 使用下划线避免与 Python 关键字冲突
    
    # 扩展字段：与Event的基础集成
    primary_event_id = Column(Integer, nullable=True, index=True)  # 主事件ID
    
    # 扩展字段：与Ledger的基础集成
    ledger_entry_id = Column(Integer, nullable=True, index=True)  # 关联的账本记录ID
    
    # 扩展字段：客户信息
    customer_id = Column(Integer, nullable=True, index=True)  # 关联的客户ID
    payment_method = Column(String(32), nullable=True)  # 支付方式
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Order(id={self.id}, shop_id={self.shop_id}, status={self.status}, amount_actual={self.amount_actual})>"

class OrderEvent(Base):
    """订单-事件关联表"""
    __tablename__ = "order_events"
    
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"<OrderEvent(order_id={self.order_id}, event_id={self.event_id})>"