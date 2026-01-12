from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from shared.db.base import Base

class Order(Base):
    """订单模型 - 业务理解层"""
    __tablename__ = "orders"
    
    id = Column(BigInteger, primary_key=True, index=True)
    shop_id = Column(BigInteger, nullable=False, index=True)
    status = Column(String(32), default="recorded")
    amount_estimate = Column(Integer, nullable=True)  # 使用整数存储分
    tags = Column(JSON)
    metadata_ = Column(JSON, name="metadata")  # 使用下划线避免与 Python 关键字冲突
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Order(id={self.id}, shop_id={self.shop_id}, status={self.status})>"

class OrderEvent(Base):
    """订单-事件关联表"""
    __tablename__ = "order_events"
    
    order_id = Column(BigInteger, ForeignKey("orders.id"), primary_key=True, nullable=False)
    event_id = Column(BigInteger, ForeignKey("events.id"), primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"<OrderEvent(order_id={self.order_id}, event_id={self.event_id})>"
