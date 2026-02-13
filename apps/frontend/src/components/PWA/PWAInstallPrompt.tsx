/**
 * PWA安装提示组件
 * 在应用可安装时显示安装提示
 */
import React, { useState } from 'react';
import { DownloadOutlined, CloseOutlined, MobileOutlined } from '@ant-design/icons';
import { Button, Modal, Typography } from 'antd';
import { usePWAInstall } from '@/hooks';

const { Text, Paragraph } = Typography;

const PWAInstallPrompt: React.FC = () => {
  const { isInstallable, isInstalled, installApp, dismissInstall } = usePWAInstall();
  const [isInstalling, setIsInstalling] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);

  if (isInstalled || !isInstallable) {
    return null;
  }

  const handleInstall = async () => {
    setIsInstalling(true);
    const success = await installApp();
    setIsInstalling(false);
    
    if (success) {
      setShowModal(false);
    }
  };

  const handleDismiss = () => {
    dismissInstall();
    setShowModal(false);
  };

  return (
    <>
      <div className="fixed bottom-20 md:bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-80 bg-white rounded-lg shadow-lg border border-gray-200 p-4 z-40">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <MobileOutlined className="text-blue-500 text-xl" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-1">
              <Text strong className="text-gray-900">安装应用</Text>
              <button
                onClick={handleDismiss}
                className="text-gray-400 hover:text-gray-600"
              >
                <CloseOutlined />
              </button>
            </div>
            <Paragraph className="text-gray-600 text-sm mb-3">
              将Dot-Store添加到主屏幕，获得更好的使用体验
            </Paragraph>
            <div className="flex gap-2">
              <Button
                type="primary"
                size="small"
                icon={<DownloadOutlined />}
                onClick={handleInstall}
                loading={isInstalling}
              >
                安装
              </Button>
              <Button size="small" onClick={handleDismiss}>
                稍后
              </Button>
            </div>
          </div>
        </div>
      </div>

      <Modal
        title="安装Dot-Store应用"
        open={showModal}
        onCancel={() => setShowModal(false)}
        footer={null}
        centered
      >
        <div className="py-4">
          <Paragraph className="text-gray-600">
            将Dot-Store安装到您的设备上，享受以下优势：
          </Paragraph>
          <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
            <li>快速访问，一键启动</li>
            <li>离线使用，无需网络</li>
            <li>全屏体验，沉浸操作</li>
            <li>推送通知，及时提醒</li>
          </ul>
          <div className="flex justify-end gap-2">
            <Button onClick={() => setShowModal(false)}>取消</Button>
            <Button type="primary" onClick={handleInstall} loading={isInstalling}>
              立即安装
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};

/**
 * iOS安装指引组件
 * 针对iOS设备显示手动安装指引
 */
export const IOSInstallGuide: React.FC = () => {
  const [showGuide, setShowGuide] = useState<boolean>(false);
  const { isInstalled } = usePWAInstall();

  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

  if (isInstalled || !isIOS) {
    return null;
  }

  return (
    <>
      <Button
        type="link"
        icon={<MobileOutlined />}
        onClick={() => setShowGuide(true)}
        className="text-gray-600"
      >
        安装应用
      </Button>

      <Modal
        title="iOS设备安装指引"
        open={showGuide}
        onCancel={() => setShowGuide(false)}
        footer={null}
        centered
      >
        <div className="py-4">
          <Paragraph className="text-gray-600 mb-4">
            请按照以下步骤将应用添加到主屏幕：
          </Paragraph>
          <ol className="list-decimal list-inside text-gray-600 space-y-3">
            <li>点击Safari浏览器底部的
              <span className="inline-block mx-1">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" className="text-gray-500">
                  <path d="M16 5l-1.42 1.42-1.59-1.59V16h-1.98V4.83L9.42 6.42 8 5l4-4 4 4zm4 5v11c0 1.1-.9 2-2 2H6c-1.11 0-2-.9-2-2V10c0-1.11.89-2 2-2h3v2H6v11h12V10h-3V8h3c1.1 0 2 .89 2 2z"/>
                </svg>
              </span>
              分享按钮
            </li>
            <li>在弹出的菜单中，向下滚动找到"添加到主屏幕"</li>
            <li>点击"添加到主屏幕"</li>
            <li>点击右上角的"添加"按钮完成安装</li>
          </ol>
        </div>
      </Modal>
    </>
  );
};

export default PWAInstallPrompt;
