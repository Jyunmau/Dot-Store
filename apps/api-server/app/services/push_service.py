"""
推送通知服务
"""
import json
import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.push import PushSubscription
from app.models.user import User
from app.core.config import settings

logger = logging.getLogger(__name__)


class PushService:
    """
    推送通知服务类
    """

    def __init__(self, db: Session):
        self.db = db
        self._webpush = None

    def _get_webpush(self):
        """
        延迟加载webpush库
        """
        if self._webpush is None:
            try:
                from pywebpush import webpush, WebPushException
                self._webpush = webpush
                self._WebPushException = WebPushException
            except ImportError:
                logger.warning("pywebpush库未安装，推送通知功能不可用")
                return None
        return self._webpush

    def subscribe(self, user_id: int, endpoint: str, p256dh: str, auth: str, user_agent: Optional[str] = None) -> PushSubscription:
        """
        订阅推送通知
        """
        existing = self.db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id,
            PushSubscription.endpoint == endpoint
        ).first()

        if existing:
            existing.p256dh = p256dh
            existing.auth = auth
            existing.user_agent = user_agent
            self.db.commit()
            self.db.refresh(existing)
            return existing

        subscription = PushSubscription(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            user_agent=user_agent
        )
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def unsubscribe(self, user_id: int, endpoint: str) -> bool:
        """
        取消订阅推送通知
        """
        subscription = self.db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id,
            PushSubscription.endpoint == endpoint
        ).first()

        if subscription:
            self.db.delete(subscription)
            self.db.commit()
            return True
        return False

    def get_user_subscriptions(self, user_id: int) -> List[PushSubscription]:
        """
        获取用户的所有订阅
        """
        return self.db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id
        ).all()

    def get_all_subscriptions(self) -> List[PushSubscription]:
        """
        获取所有订阅
        """
        return self.db.query(PushSubscription).all()

    def send_notification(
        self,
        subscription: PushSubscription,
        title: str,
        body: str,
        icon: Optional[str] = None,
        url: Optional[str] = None
    ) -> bool:
        """
        发送推送通知
        """
        webpush = self._get_webpush()
        if not webpush:
            logger.warning("推送服务不可用")
            return False

        if not settings.VAPID_PRIVATE_KEY or not settings.VAPID_PUBLIC_KEY:
            logger.warning("VAPID密钥未配置")
            return False

        payload = {
            "title": title,
            "body": body,
            "icon": icon or "/icons/icon-192x192.png",
            "url": url or "/"
        }

        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth
            }
        }

        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": settings.VAPID_SUBJECT,
                }
            )
            logger.info(f"推送通知发送成功: {subscription.id}")
            return True
        except Exception as e:
            logger.error(f"推送通知发送失败: {e}")
            return False

    def send_to_user(
        self,
        user_id: int,
        title: str,
        body: str,
        icon: Optional[str] = None,
        url: Optional[str] = None
    ) -> int:
        """
        向指定用户发送推送通知
        返回成功发送的数量
        """
        subscriptions = self.get_user_subscriptions(user_id)
        success_count = 0

        for subscription in subscriptions:
            if self.send_notification(subscription, title, body, icon, url):
                success_count += 1

        return success_count

    def send_to_all(
        self,
        title: str,
        body: str,
        icon: Optional[str] = None,
        url: Optional[str] = None
    ) -> int:
        """
        向所有订阅者发送推送通知
        返回成功发送的数量
        """
        subscriptions = self.get_all_subscriptions()
        success_count = 0

        for subscription in subscriptions:
            if self.send_notification(subscription, title, body, icon, url):
                success_count += 1

        return success_count

    def send_to_users(
        self,
        user_ids: List[int],
        title: str,
        body: str,
        icon: Optional[str] = None,
        url: Optional[str] = None
    ) -> int:
        """
        向指定用户列表发送推送通知
        返回成功发送的数量
        """
        success_count = 0

        for user_id in user_ids:
            success_count += self.send_to_user(user_id, title, body, icon, url)

        return success_count


def generate_vapid_keys() -> tuple:
    """
    生成VAPID密钥对
    返回 (public_key, private_key)
    """
    try:
        from py_vapid import Vapid
        vapid = Vapid()
        vapid.generate_keys()
        public_key = vapid.public_key.public_bytes(
            encoding=4
        ).decode('utf-8')
        private_key = vapid.private_key.private_bytes(
            encoding=4
        ).decode('utf-8')
        return public_key, private_key
    except ImportError:
        logger.error("py_vapid库未安装，无法生成VAPID密钥")
        return "", ""
