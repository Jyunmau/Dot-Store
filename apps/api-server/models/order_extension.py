from sqlalchemy import Column, Integer, String, TIMESTAMP, NUMERIC, JSON, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class OrderItem(Base):
    """订单项目模型 - Platform层核心模块，用于记录订单中的具体菜品/酒水项目"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)  # 关联的订单ID
    
    # 项目基本信息
    item_name = Column(String(128), nullable=False)  # 菜品/酒水名称
    item_type = Column(String(32), nullable=False, index=True)  # 项目类型：drink, food, snack, etc.
    
    # 项目业务属性
    quantity = Column(Integer, nullable=False, default=1)  # 数量
    unit_price = Column(NUMERIC(12, 2), nullable=False)  # 单价
    total_price = Column(NUMERIC(12, 2), nullable=False)  # 总价
    
    # 项目扩展信息
    item_metadata = Column(JSON, nullable=True)  # 项目元数据：如酒水品牌、菜品口味等
    is_complementary = Column(Integer, default=0)  # 是否赠送：0: 正常, 1: 赠送
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, shop_id={self.shop_id}, order_id={self.order_id}, item_name={self.item_name}, quantity={self.quantity}, total_price={self.total_price})>"

class OrderTableAssociation(Base):
    """订单-酒台关联模型 - Platform层核心模块，用于记录订单关联的酒台信息"""
    __tablename__ = "order_table_associations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)  # 关联的订单ID
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)  # 关联的酒台ID
    
    # 关联信息
    start_time = Column(TIMESTAMP(timezone=True), nullable=True)  # 开始使用时间
    end_time = Column(TIMESTAMP(timezone=True), nullable=True)  # 结束使用时间
    duration = Column(Integer, nullable=True)  # 使用时长（分钟）
    
    def __repr__(self):
        return f"<OrderTableAssociation(id={self.id}, shop_id={self.shop_id}, order_id={self.order_id}, table_id={self.table_id})>"

class OrderPayment(Base):
    """订单支付记录模型 - Platform层核心模块，用于记录订单的支付历史"""
    __tablename__ = "order_payments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)  # 关联的订单ID
    
    # 支付基本信息
    payment_no = Column(String(64), nullable=False, index=True, unique=True)  # 支付流水号
    amount = Column(NUMERIC(12, 2), nullable=False)  # 支付金额
    currency = Column(String(16), default="CNY")  # 货币类型
    payment_method = Column(String(32), nullable=False, index=True)  # 支付方式：wechat, alipay, cash, etc.
    
    # 支付状态
    status = Column(String(32), nullable=False, index=True)  # 支付状态：pending, completed, failed, refunded, partial_refunded
    
    # 支付时间
    payment_time = Column(TIMESTAMP(timezone=True), nullable=True)  # 实际支付时间
    
    # 支付扩展信息
    transaction_id = Column(String(64), nullable=True, index=True, unique=True)  # 第三方支付平台交易ID
    payment_details = Column(JSON, nullable=True)  # 支付详情
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<OrderPayment(id={self.id}, shop_id={self.shop_id}, order_id={self.order_id}, payment_no={self.payment_no}, amount={self.amount}, status={self.status})>"
