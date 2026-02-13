/**
 * 推送通知服务
 * 处理Web Push订阅和通知功能
 */
import apiClient from './apiClient';

interface PushSubscriptionKeys {
  p256dh: string;
  auth: string;
}

interface PushSubscriptionData {
  endpoint: string;
  keys: PushSubscriptionKeys;
}

interface VAPIDPublicKeyResponse {
  public_key: string;
}

class PushNotificationService {
  private registration: ServiceWorkerRegistration | null = null;

  /**
   * 初始化服务
   */
  async init(): Promise<boolean> {
    if (!('serviceWorker' in navigator)) {
      console.log('[Push] Service Worker不支持');
      return false;
    }

    if (!('PushManager' in window)) {
      console.log('[Push] Push API不支持');
      return false;
    }

    try {
      this.registration = await navigator.serviceWorker.ready;
      console.log('[Push] Service Worker已就绪');
      return true;
    } catch (error) {
      console.error('[Push] Service Worker初始化失败:', error);
      return false;
    }
  }

  /**
   * 检查通知权限
   */
  async checkPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      return 'denied';
    }
    return Notification.permission;
  }

  /**
   * 请求通知权限
   */
  async requestPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      console.log('[Push] Notification API不支持');
      return 'denied';
    }

    const permission = await Notification.requestPermission();
    console.log('[Push] 通知权限:', permission);
    return permission;
  }

  /**
   * 获取VAPID公钥
   */
  async getVAPIDPublicKey(): Promise<string | null> {
    try {
      const response = await apiClient.get<VAPIDPublicKeyResponse>('/push/vapid-public-key');
      return response.data.public_key;
    } catch (error) {
      console.error('[Push] 获取VAPID公钥失败:', error);
      return null;
    }
  }

  /**
   * 订阅推送通知
   */
  async subscribe(): Promise<boolean> {
    if (!this.registration) {
      const initialized = await this.init();
      if (!initialized) {
        return false;
      }
    }

    const permission = await this.requestPermission();
    if (permission !== 'granted') {
      console.log('[Push] 通知权限未授予');
      return false;
    }

    const vapidPublicKey = await this.getVAPIDPublicKey();
    if (!vapidPublicKey) {
      console.log('[Push] VAPID公钥不可用');
      return false;
    }

    try {
      const subscription = await this.registration!.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(vapidPublicKey).buffer as ArrayBuffer
      });

      console.log('[Push] 订阅成功:', subscription.endpoint);

      const subscriptionData: PushSubscriptionData = {
        endpoint: subscription.endpoint,
        keys: {
          p256dh: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('p256dh')!))),
          auth: btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('auth')!)))
        }
      };

      await apiClient.post('/push/subscribe', subscriptionData);
      console.log('[Push] 订阅信息已发送到服务器');
      return true;
    } catch (error) {
      console.error('[Push] 订阅失败:', error);
      return false;
    }
  }

  /**
   * 取消订阅
   */
  async unsubscribe(): Promise<boolean> {
    if (!this.registration) {
      return false;
    }

    try {
      const subscription = await this.registration.pushManager.getSubscription();
      
      if (subscription) {
        await subscription.unsubscribe();
        await apiClient.delete('/push/subscribe', {
          params: { endpoint: subscription.endpoint }
        });
        console.log('[Push] 取消订阅成功');
      }
      
      return true;
    } catch (error) {
      console.error('[Push] 取消订阅失败:', error);
      return false;
    }
  }

  /**
   * 检查是否已订阅
   */
  async isSubscribed(): Promise<boolean> {
    if (!this.registration) {
      await this.init();
    }

    if (!this.registration) {
      return false;
    }

    try {
      const subscription = await this.registration.pushManager.getSubscription();
      return subscription !== null;
    } catch (error) {
      return false;
    }
  }

  /**
   * 发送测试通知
   */
  async sendTestNotification(): Promise<boolean> {
    try {
      await apiClient.post('/push/test');
      return true;
    } catch (error) {
      console.error('[Push] 发送测试通知失败:', error);
      return false;
    }
  }

  /**
   * Base64 URL转换为Uint8Array
   */
  private urlBase64ToUint8Array(base64String: string): Uint8Array {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }
}

export const pushNotificationService = new PushNotificationService();
export default pushNotificationService;
