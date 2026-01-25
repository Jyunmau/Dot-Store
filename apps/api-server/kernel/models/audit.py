from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from .base import Base

class AuditLog(Base):
    """审计日志模型 - Kernel层核心模块，用于记录所有关键操作的审计日志"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    
    # 操作人信息
    account_id = Column(Integer, nullable=True, index=True)  # 操作人账户ID
    account_type = Column(String(32), nullable=True)  # 操作人类型：user, admin, system
    actor_ip = Column(String(64), nullable=True)  # 操作人IP地址
    actor_agent = Column(String(256), nullable=True)  # 操作人用户代理
    
    # 操作信息
    action = Column(String(64), nullable=False)  # 操作类型：create, update, delete, login, logout, etc.
    resource_type = Column(String(64), nullable=False, index=True)  # 资源类型：order, event, ledger, resource, etc.
    resource_id = Column(Integer, nullable=True, index=True)  # 资源ID
    
    # 操作详情
    details = Column(JSON, nullable=True)  # 操作详情，包含before和after状态
    change_summary = Column(String(256), nullable=True)  # 操作变更摘要
    
    # 操作结果
    result = Column(String(32), default="success")  # success, failed, partial
    error_message = Column(String(512), nullable=True)  # 错误信息，仅当操作失败时记录
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, shop_id={self.shop_id}, action={self.action}, resource_type={self.resource_type}, resource_id={self.resource_id}, result={self.result})>"