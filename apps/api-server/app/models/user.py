"""
Dot-Store V2.1 用户数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from ..core.database import Base


class User(Base):
    """
    用户模型
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String(32), unique=True, nullable=True, index=True)
    email = Column(String(128), unique=True, nullable=True, index=True)
    password_hash = Column(String(256), nullable=False)
    shop_name = Column(String(128), nullable=False)
    shop_type = Column(String(32), nullable=False)
    city = Column(String(64), nullable=False)
    role = Column(String(32), nullable=False, default="owner")
    status = Column(String(32), nullable=False, default="active", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, nullable=False, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # 店员权限（JSON格式存储）
    permissions = Column(Text, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone}, email={self.email}, role={self.role})>"

    def is_locked(self) -> bool:
        """
        检查账户是否被锁定
        """
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until

    def is_owner(self) -> bool:
        """
        检查是否为店主
        """
        return self.role == "owner"

    def is_active(self) -> bool:
        """
        检查账户是否活跃
        """
        return self.status == "active"
