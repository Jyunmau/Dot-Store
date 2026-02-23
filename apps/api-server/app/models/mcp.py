"""
Dot-Store V2.2 MCP服务数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base


class MCPSession(Base):
    """
    MCP会话模型
    """
    __tablename__ = "mcp_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(64), unique=True, nullable=False, index=True)
    api_key_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    client_info = Column(JSONB, nullable=True)
    status = Column(String(32), nullable=False, default="active", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_active_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    api_key_user = relationship("User", foreign_keys=[api_key_id])

    def __repr__(self):
        return f"<MCPSession(id={self.id}, session_id={self.session_id}, status={self.status})>"

    def is_expired(self) -> bool:
        """
        检查会话是否过期
        """
        return datetime.utcnow() > self.expires_at

    def is_active(self) -> bool:
        """
        检查会话是否活跃
        """
        return self.status == "active" and not self.is_expired()


class MCPOperationLog(Base):
    """
    MCP操作日志模型
    """
    __tablename__ = "mcp_operation_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(64), nullable=False, index=True)
    operation_type = Column(String(32), nullable=False, index=True)
    tool_name = Column(String(64), nullable=True)
    resource_uri = Column(String(256), nullable=True)
    input_params = Column(JSONB, nullable=True)
    output_result = Column(JSONB, nullable=True)
    status = Column(String(32), nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<MCPOperationLog(id={self.id}, operation_type={self.operation_type}, status={self.status})>"
