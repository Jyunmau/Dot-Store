"""
Dot-Store V2.2 用户偏好配置服务
实现用户偏好配置的管理功能
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.user_preference import UserPreference
from app.services.event_service import EventService


class UserPreferenceService:
    """用户偏好配置服务"""
    
    @staticmethod
    def get_or_create(db: Session, user_id: int) -> UserPreference:
        """
        获取或创建用户偏好配置
        """
        preference = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not preference:
            preference = UserPreference(
                user_id=user_id,
                weekly_reminder_enabled=True,
                weekly_reminder_day=1,
                weekly_reminder_time=datetime.strptime("10:00", "%H:%M").time(),
                monthly_report_enabled=True,
                monthly_report_day=1,
                monthly_report_time=datetime.strptime("09:00", "%H:%M").time(),
                risk_alert_enabled=True,
                risk_alert_threshold='medium',
                notification_channels=['push']
            )
            db.add(preference)
            db.commit()
            db.refresh(preference)
            
            EventService.log(
                db=db,
                user_id=user_id,
                event_type='user_preference_created',
                entity_type='user_preference',
                entity_id=preference.id,
                operator_id=user_id
            )
        
        return preference
    
    @staticmethod
    def update(
        db: Session, 
        user_id: int, 
        **kwargs
    ) -> Optional[UserPreference]:
        """
        更新用户偏好配置
        """
        preference = UserPreferenceService.get_or_create(db, user_id)
        
        time_fields = ['weekly_reminder_time', 'monthly_report_time']
        
        for key, value in kwargs.items():
            if value is not None and hasattr(preference, key):
                if key in time_fields and isinstance(value, str):
                    try:
                        value = datetime.strptime(value, "%H:%M").time()
                    except ValueError:
                        continue
                setattr(preference, key, value)
        
        preference.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(preference)
        
        EventService.log(
            db=db,
            user_id=user_id,
            event_type='user_preference_updated',
            entity_type='user_preference',
            entity_id=preference.id,
            operator_id=user_id
        )
        
        return preference
    
    @staticmethod
    def update_weekly_reminder(
        db: Session,
        user_id: int,
        enabled: Optional[bool] = None,
        day: Optional[int] = None,
        time_str: Optional[str] = None
    ) -> Optional[UserPreference]:
        """
        更新周提醒设置
        """
        kwargs = {}
        if enabled is not None:
            kwargs['weekly_reminder_enabled'] = enabled
        if day is not None:
            kwargs['weekly_reminder_day'] = day
        if time_str is not None:
            kwargs['weekly_reminder_time'] = time_str
        
        return UserPreferenceService.update(db, user_id, **kwargs)
    
    @staticmethod
    def update_monthly_report(
        db: Session,
        user_id: int,
        enabled: Optional[bool] = None,
        day: Optional[int] = None,
        time_str: Optional[str] = None
    ) -> Optional[UserPreference]:
        """
        更新月度报告设置
        """
        kwargs = {}
        if enabled is not None:
            kwargs['monthly_report_enabled'] = enabled
        if day is not None:
            kwargs['monthly_report_day'] = day
        if time_str is not None:
            kwargs['monthly_report_time'] = time_str
        
        return UserPreferenceService.update(db, user_id, **kwargs)
    
    @staticmethod
    def update_risk_alert(
        db: Session,
        user_id: int,
        enabled: Optional[bool] = None,
        threshold: Optional[str] = None
    ) -> Optional[UserPreference]:
        """
        更新风险预警设置
        """
        kwargs = {}
        if enabled is not None:
            kwargs['risk_alert_enabled'] = enabled
        if threshold is not None:
            kwargs['risk_alert_threshold'] = threshold
        
        return UserPreferenceService.update(db, user_id, **kwargs)
    
    @staticmethod
    def update_notification_channels(
        db: Session,
        user_id: int,
        channels: List[str]
    ) -> Optional[UserPreference]:
        """
        更新通知渠道
        """
        valid_channels = ['push', 'email', 'sms']
        filtered_channels = [c for c in channels if c in valid_channels]
        
        if not filtered_channels:
            filtered_channels = ['push']
        
        return UserPreferenceService.update(
            db, user_id, 
            notification_channels=filtered_channels
        )
    
    @staticmethod
    def reset_to_default(db: Session, user_id: int) -> UserPreference:
        """
        重置为默认设置
        """
        preference = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if preference:
            preference.weekly_reminder_enabled = True
            preference.weekly_reminder_day = 1
            preference.weekly_reminder_time = datetime.strptime("10:00", "%H:%M").time()
            preference.monthly_report_enabled = True
            preference.monthly_report_day = 1
            preference.monthly_report_time = datetime.strptime("09:00", "%H:%M").time()
            preference.risk_alert_enabled = True
            preference.risk_alert_threshold = 'medium'
            preference.notification_channels = ['push']
            preference.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(preference)
            
            EventService.log(
                db=db,
                user_id=user_id,
                event_type='user_preference_reset',
                entity_type='user_preference',
                entity_id=preference.id,
                operator_id=user_id
            )
        else:
            preference = UserPreferenceService.get_or_create(db, user_id)
        
        return preference
