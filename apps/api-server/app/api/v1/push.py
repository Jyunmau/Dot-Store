"""
推送通知API
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.push import (
    PushSubscriptionCreate,
    PushSubscriptionResponse,
    PushNotificationRequest,
    VAPIDPublicKeyResponse
)
from app.services.push_service import PushService
from app.core.config import settings

router = APIRouter(prefix="/push", tags=["推送通知"])


@router.get("/vapid-public-key", response_model=VAPIDPublicKeyResponse)
async def get_vapid_public_key():
    """
    获取VAPID公钥
    """
    if not settings.VAPID_PUBLIC_KEY:
        raise HTTPException(status_code=503, detail="推送服务未配置")
    
    return VAPIDPublicKeyResponse(public_key=settings.VAPID_PUBLIC_KEY)


@router.post("/subscribe", response_model=PushSubscriptionResponse)
async def subscribe_push(
    subscription: PushSubscriptionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    订阅推送通知
    """
    push_service = PushService(db)
    user_agent = request.headers.get("user-agent")
    
    new_subscription = push_service.subscribe(
        user_id=current_user.id,
        endpoint=subscription.endpoint,
        p256dh=subscription.keys.p256dh,
        auth=subscription.keys.auth,
        user_agent=user_agent
    )
    
    return PushSubscriptionResponse(
        id=new_subscription.id,
        endpoint=new_subscription.endpoint,
        created_at=new_subscription.created_at
    )


@router.delete("/subscribe")
async def unsubscribe_push(
    endpoint: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    取消订阅推送通知
    """
    push_service = PushService(db)
    success = push_service.unsubscribe(
        user_id=current_user.id,
        endpoint=endpoint
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="订阅不存在")
    
    return {"message": "取消订阅成功"}


@router.get("/subscriptions", response_model=List[PushSubscriptionResponse])
async def get_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有订阅
    """
    push_service = PushService(db)
    subscriptions = push_service.get_user_subscriptions(current_user.id)
    
    return [
        PushSubscriptionResponse(
            id=sub.id,
            endpoint=sub.endpoint,
            created_at=sub.created_at
        )
        for sub in subscriptions
    ]


@router.post("/send")
async def send_push_notification(
    notification: PushNotificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发送推送通知（仅限店主）
    """
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="无权限发送推送通知")
    
    push_service = PushService(db)
    
    if notification.user_ids:
        success_count = push_service.send_to_users(
            user_ids=notification.user_ids,
            title=notification.title,
            body=notification.body,
            icon=notification.icon,
            url=notification.url
        )
    else:
        success_count = push_service.send_to_all(
            title=notification.title,
            body=notification.body,
            icon=notification.icon,
            url=notification.url
        )
    
    return {
        "message": f"推送通知发送完成",
        "success_count": success_count
    }


@router.post("/test")
async def test_push_notification(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    测试推送通知
    """
    push_service = PushService(db)
    
    success_count = push_service.send_to_user(
        user_id=current_user.id,
        title="测试通知",
        body="这是一条测试推送通知",
        url="/"
    )
    
    if success_count == 0:
        return {"message": "没有可用的订阅或推送服务未配置"}
    
    return {"message": f"测试通知发送成功", "success_count": success_count}
