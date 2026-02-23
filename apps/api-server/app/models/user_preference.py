"""
Dot-Store V2.2 用户偏好配置模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base


class UserPreference(Base):
    """
    用户偏好配置模型
    存储用户的提醒设置和个性化配置
    """
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    weekly_reminder_enabled = Column(Boolean, nullable=False, default=True)
    weekly_reminder_day = Column(Integer, nullable=False, default=1)
    weekly_reminder_time = Column(Time, nullable=False, default=datetime.strptime("10:00", "%H:%M").time())
    
    monthly_report_enabled = Column(Boolean, nullable=False, default=True)
    monthly_report_day = Column(Integer, nullable=False, default=1)
    monthly_report_time = Column(Time, nullable=False, default=datetime.strptime("09:00", "%H:%M").time())
    
    risk_alert_enabled = Column(Boolean, nullable=False, default=True)
    risk_alert_threshold = Column(String(32), nullable=False, default='medium')
    
    notification_channels = Column(JSONB, nullable=False, default=list)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id})>"

    def to_dict(self):
        """
        转换为字典格式
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'weekly_reminder_enabled': self.weekly_reminder_enabled,
            'weekly_reminder_day': self.weekly_reminder_day,
            'weekly_reminder_time': self.weekly_reminder_time.strftime('%H:%M') if self.weekly_reminder_time else '10:00',
            'monthly_report_enabled': self.monthly_report_enabled,
            'monthly_report_day': self.monthly_report_day,
            'monthly_report_time': self.monthly_report_time.strftime('%H:%M') if self.monthly_report_time else '09:00',
            'risk_alert_enabled': self.risk_alert_enabled,
            'risk_alert_threshold': self.risk_alert_threshold,
            'notification_channels': self.notification_channels or ['push'],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
