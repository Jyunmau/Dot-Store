from sqlalchemy import Column, Integer, String, NUMERIC, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class CashbackPolicy(Base):
    """返现规则模型 - Platform层核心模块，用于管理返现规则"""
    __tablename__ = "cashback_policies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 规则基本信息
    name = Column(String(64), nullable=False)  # 规则名称
    description = Column(String(256), nullable=True)  # 规则描述
    
    # 规则类型
    policy_type = Column(String(32), nullable=False, index=True)  # 规则类型：percentage, fixed_amount, tiered
    status = Column(String(32), default="active", index=True)  # 规则状态：active, inactive, expired
    
    # 规则条件
    min_spend = Column(NUMERIC(12, 2), nullable=True)  # 最低消费金额
    max_cashback = Column(NUMERIC(12, 2), nullable=True)  # 最高返现金额
    
    # 规则参数
    cashback_value = Column(NUMERIC(12, 2), nullable=True)  # 返现值：百分比或固定金额
    
    # 层级返现规则（JSON格式）
    # 示例：[{"min": 0, "max": 100, "value": 5}, {"min": 100, "max": 500, "value": 8}, {"min": 500, "value": 10}]
    tiered_rules = Column(JSON, nullable=True)  # 层级返现规则，仅当policy_type为tiered时使用
    
    # 适用范围
    applicable_to = Column(String(32), default="all")  # 适用对象：all, member, shareholder, vip
    applicable_areas = Column(JSON, nullable=True)  # 适用区域：["A", "B"]
    applicable_tables = Column(JSON, nullable=True)  # 适用酒台：[1, 2, 3]
    
    # 时间范围
    valid_from = Column(TIMESTAMP(timezone=True), nullable=False, index=True)  # 生效时间
    valid_to = Column(TIMESTAMP(timezone=True), nullable=True, index=True)  # 失效时间
    
    # 操作信息
    created_by = Column(Integer, nullable=True)  # 创建人ID
    updated_by = Column(Integer, nullable=True)  # 更新人ID
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<CashbackPolicy(id={self.id}, shop_id={self.shop_id}, name={self.name}, policy_type={self.policy_type}, status={self.status})>"

class RedemptionPolicy(Base):
    """积分抵扣规则模型 - Platform层核心模块，用于管理积分抵扣规则"""
    __tablename__ = "redemption_policies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 规则基本信息
    name = Column(String(64), nullable=False)  # 规则名称
    description = Column(String(256), nullable=True)  # 规则描述
    
    # 规则类型
    policy_type = Column(String(32), nullable=False, index=True)  # 规则类型：points_to_cash, points_exchange
    status = Column(String(32), default="active", index=True)  # 规则状态：active, inactive, expired
    
    # 规则参数
    points_per_unit = Column(Integer, nullable=False)  # 每单位价值所需积分：例如100积分=1元
    min_points = Column(Integer, nullable=True)  # 最低抵扣积分
    max_points_per_order = Column(Integer, nullable=True)  # 每单最高抵扣积分
    max_discount_ratio = Column(NUMERIC(5, 2), nullable=True)  # 最高抵扣比例：例如0.5表示最多抵扣订单金额的50%
    
    # 适用范围
    applicable_to = Column(String(32), default="all")  # 适用对象：all, member, shareholder, vip
    
    # 时间范围
    valid_from = Column(TIMESTAMP(timezone=True), nullable=False, index=True)  # 生效时间
    valid_to = Column(TIMESTAMP(timezone=True), nullable=True, index=True)  # 失效时间
    
    # 操作信息
    created_by = Column(Integer, nullable=True)  # 创建人ID
    updated_by = Column(Integer, nullable=True)  # 更新人ID
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<RedemptionPolicy(id={self.id}, shop_id={self.shop_id}, name={self.name}, policy_type={self.policy_type}, status={self.status})>"

class CashbackRecord(Base):
    """返现记录模型 - Platform层核心模块，用于记录返现历史"""
    __tablename__ = "cashback_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 返现基本信息
    customer_id = Column(Integer, nullable=False, index=True)  # 返现对象ID
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)  # 关联订单ID
    cashback_policy_id = Column(Integer, ForeignKey("cashback_policies.id"), nullable=False, index=True)  # 应用的返现规则ID
    
    # 返现金额信息
    order_amount = Column(NUMERIC(12, 2), nullable=False)  # 订单金额
    cashback_amount = Column(NUMERIC(12, 2), nullable=False)  # 返现金额
    cashback_percentage = Column(NUMERIC(5, 2), nullable=True)  # 返现百分比
    
    # 返现状态
    status = Column(String(32), default="processed", index=True)  # 返现状态：processed, failed, reversed
    
    # 与Ledger模块的集成
    ledger_entry_id = Column(Integer, nullable=True, index=True)  # 关联的LedgerEntry ID
    
    # 操作信息
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<CashbackRecord(id={self.id}, shop_id={self.shop_id}, customer_id={self.customer_id}, order_id={self.order_id}, cashback_amount={self.cashback_amount})>"

class RedemptionRecord(Base):
    """积分抵扣记录模型 - Platform层核心模块，用于记录积分抵扣历史"""
    __tablename__ = "redemption_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 抵扣基本信息
    customer_id = Column(Integer, nullable=False, index=True)  # 抵扣对象ID
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)  # 关联订单ID
    redemption_policy_id = Column(Integer, ForeignKey("redemption_policies.id"), nullable=False, index=True)  # 应用的抵扣规则ID
    
    # 抵扣金额信息
    points_redeemed = Column(Integer, nullable=False)  # 抵扣积分
    equivalent_cash = Column(NUMERIC(12, 2), nullable=False)  # 等值现金
    order_amount = Column(NUMERIC(12, 2), nullable=False)  # 订单金额
    actual_paid = Column(NUMERIC(12, 2), nullable=False)  # 实际支付金额
    
    # 抵扣状态
    status = Column(String(32), default="processed", index=True)  # 抵扣状态：processed, failed, reversed
    
    # 与Ledger模块的集成
    ledger_entry_id = Column(Integer, nullable=True, index=True)  # 关联的LedgerEntry ID
    
    # 操作信息
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<RedemptionRecord(id={self.id}, shop_id={self.shop_id}, customer_id={self.customer_id}, order_id={self.order_id}, points_redeemed={self.points_redeemed}, equivalent_cash={self.equivalent_cash})>"
