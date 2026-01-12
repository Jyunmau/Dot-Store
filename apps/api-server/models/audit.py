from sqlalchemy import Column, BigInteger, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from .base import Base

class AuditLog(Base):
    """审计日志模型"""
    __tablename__ = "audit_logs"
    
    id = Column(BigInteger, primary_key=True, index=True)
    entity_type = Column(String(32), nullable=False, index=True)  # orders, ledger_entries 等
    entity_id = Column(BigInteger, nullable=False, index=True)
    action = Column(String(32), nullable=False)  # create, update, delete
    before_data = Column(JSON)  # 修改前的数据
    after_data = Column(JSON)  # 修改后的数据
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, entity_type={self.entity_type}, entity_id={self.entity_id}, action={self.action})>"
