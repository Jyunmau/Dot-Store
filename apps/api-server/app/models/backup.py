"""
Dot-Store V2.1 备份数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class Backup(Base):
    """
    备份模型
    """
    __tablename__ = "backups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="pending", index=True)
    backup_path = Column(String(256), nullable=False)
    backup_size = Column(Integer, default=0)
    backup_type = Column(String(32), nullable=False, default="manual", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Backup(id={self.id}, user_id={self.user_id}, name={self.name}, status={self.status})>"

    def is_completed(self) -> bool:
        """
        检查备份是否已完成
        """
        return self.status == "completed"

    def is_pending(self) -> bool:
        """
        检查备份是否等待中
        """
        return self.status == "pending"

    def is_failed(self) -> bool:
        """
        检查备份是否失败
        """
        return self.status == "failed"


class BackupSettings(Base):
    """
    备份设置模型
    """
    __tablename__ = "backup_settings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    auto_backup_enabled = Column(Boolean, default=False)
    backup_schedule = Column(String(128), default="0 0 * * *")
    backup_retention_days = Column(Integer, default=7)
    last_auto_backup_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BackupSettings(id={self.id}, user_id={self.user_id}, auto_backup_enabled={self.auto_backup_enabled})>"
