/**
 * 网络状态检测Hook
 * 监听网络连接状态变化，提供在线/离线状态
 */
import { useState, useEffect } from 'react';

interface UseOnlineStatusReturn {
  isOnline: boolean;
  isOffline: boolean;
}

export const useOnlineStatus = (): UseOnlineStatusReturn => {
  const [isOnline, setIsOnline] = useState<boolean>(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      console.log('[Network] 已连接到网络');
    };

    const handleOffline = () => {
      setIsOnline(false);
      console.log('[Network] 网络连接已断开');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return {
    isOnline,
    isOffline: !isOnline,
  };
};

export default useOnlineStatus;
