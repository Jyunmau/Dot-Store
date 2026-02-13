/**
 * 离线状态提示组件
 * 在网络断开时显示提示条
 */
import React from 'react';
import { WifiOutlined, DisconnectOutlined } from '@ant-design/icons';
import { useOnlineStatus } from '@/hooks';

const OfflineIndicator: React.FC = () => {
  const { isOffline } = useOnlineStatus();

  if (!isOffline) {
    return null;
  }

  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-amber-500 text-white py-2 px-4 flex items-center justify-center gap-2 text-sm">
      <DisconnectOutlined />
      <span>网络连接已断开，部分功能可能不可用</span>
    </div>
  );
};

/**
 * 网络状态指示器组件
 * 显示当前网络状态
 */
export const NetworkStatus: React.FC = () => {
  const { isOnline } = useOnlineStatus();

  return (
    <div className="flex items-center gap-2 text-sm">
      {isOnline ? (
        <>
          <WifiOutlined className="text-green-500" />
          <span className="text-gray-600">已连接</span>
        </>
      ) : (
        <>
          <DisconnectOutlined className="text-amber-500" />
          <span className="text-amber-600">离线</span>
        </>
      )}
    </div>
  );
};

export default OfflineIndicator;
