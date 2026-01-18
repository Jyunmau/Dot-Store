from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from .base import Base

class Account(Base):
    """账户模型 - Kernel层核心模块，支持会员和管理员角色"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, nullable=False, index=True)
    username = Column(String(64), nullable=True, index=True, unique=True)  # 用户名，可选
    phone = Column(String(32), nullable=True, index=True, unique=True)  # 手机号，用于登录和验证
    email = Column(String(128), nullable=True, index=True, unique=True)  # 邮箱，可选
    password_hash = Column(String(256), nullable=True)  # 密码哈希，仅用于需要密码登录的账户
    
    # 角色管理：支持多种角色
    role = Column(String(32), default="user")  # user, admin, system, member, shareholder
    
    # 账户状态
    status = Column(String(32), default="active")  # active, inactive, suspended, deleted
    
    # 扩展字段：关联的客户/会员信息
    profile_id = Column(Integer, nullable=True, index=True)  # 关联的用户资料ID
    profile_type = Column(String(32), nullable=True)  # 关联的用户资料类型：member, customer, admin
    
    # 认证相关字段
    last_login_at = Column(TIMESTAMP(timezone=True), nullable=True)  # 最后登录时间
    login_attempts = Column(Integer, default=0)  # 登录尝试次数
    locked_until = Column(TIMESTAMP(timezone=True), nullable=True)  # 账户锁定时间
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Account(id={self.id}, shop_id={self.shop_id}, phone={self.phone}, role={self.role}, status={self.status})>"

class AuthToken(Base):
    """认证令牌模型 - 管理JWT令牌"""
    __tablename__ = "auth_tokens"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, nullable=False, index=True)
    token = Column(String(512), nullable=False, unique=True)  # JWT令牌
    token_type = Column(String(32), default="access")  # access, refresh
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)  # 令牌过期时间
    ip_address = Column(String(64), nullable=True)  # 生成令牌的IP地址
    user_agent = Column(String(256), nullable=True)  # 生成令牌的用户代理
    is_revoked = Column(Integer, default=0)  # 0: 有效, 1: 已撤销
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<AuthToken(id={self.id}, account_id={self.account_id}, token_type={self.token_type}, is_revoked={self.is_revoked})>"
