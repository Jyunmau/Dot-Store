"""
推送订阅Schema
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PushSubscriptionKeys(BaseModel):
    """
    推送订阅密钥
    """
    p256dh: str
    auth: str


class PushSubscriptionCreate(BaseModel):
    """
    创建推送订阅请求
    """
    endpoint: str
    keys: PushSubscriptionKeys


class PushSubscriptionResponse(BaseModel):
    """
    推送订阅响应
    """
    id: int
    endpoint: str
    created_at: datetime

    class Config:
        from_attributes = True


class PushNotificationRequest(BaseModel):
    """
    推送通知请求
    """
    title: str
    body: str
    icon: Optional[str] = None
    url: Optional[str] = None
    user_ids: Optional[list[int]] = None


class VAPIDPublicKeyResponse(BaseModel):
    """
    VAPID公钥响应
    """
    public_key: str
