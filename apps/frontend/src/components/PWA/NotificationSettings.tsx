/**
 * 通知设置组件
 * 管理推送通知订阅
 */
import React, { useState, useEffect } from 'react';
import { Card, Switch, Button, Typography, message, Alert } from 'antd';
import { BellOutlined, BellFilled, CheckCircleOutlined } from '@ant-design/icons';
import { pushNotificationService } from '@/services';

const { Text, Paragraph } = Typography;

const NotificationSettings: React.FC = () => {
  const [isEnabled, setIsEnabled] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [permission, setPermission] = useState<NotificationPermission>('default');

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    const perm = await pushNotificationService.checkPermission();
    setPermission(perm);
    
    const subscribed = await pushNotificationService.isSubscribed();
    setIsEnabled(subscribed);
  };

  const handleToggle = async (checked: boolean) => {
    setIsLoading(true);
    
    try {
      if (checked) {
        const success = await pushNotificationService.subscribe();
        if (success) {
          setIsEnabled(true);
          message.success('推送通知已开启');
        } else {
          message.error('开启推送通知失败');
        }
      } else {
        const success = await pushNotificationService.unsubscribe();
        if (success) {
          setIsEnabled(false);
          message.success('推送通知已关闭');
        } else {
          message.error('关闭推送通知失败');
        }
      }
    } catch (error) {
      message.error('操作失败，请重试');
    } finally {
      setIsLoading(false);
      checkStatus();
    }
  };

  const handleTest = async () => {
    setIsLoading(true);
    
    try {
      const success = await pushNotificationService.sendTestNotification();
      if (success) {
        message.success('测试通知已发送');
      } else {
        message.error('发送测试通知失败');
      }
    } catch (error) {
      message.error('发送测试通知失败');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card title={<><BellOutlined /> 通知设置</>} className="mb-4">
      {permission === 'denied' && (
        <Alert
          type="warning"
          message="通知权限被拒绝"
          description="请在浏览器设置中允许通知权限"
          showIcon
          className="mb-4"
        />
      )}
      
      <div className="flex items-center justify-between py-4 border-b border-gray-100">
        <div>
          <Text strong>推送通知</Text>
          <Paragraph className="text-gray-500 text-sm mb-0">
            接收订单提醒、库存预警等重要通知
          </Paragraph>
        </div>
        <Switch
          checked={isEnabled}
          onChange={handleToggle}
          loading={isLoading}
          disabled={permission === 'denied'}
        />
      </div>

      {isEnabled && (
        <div className="flex items-center justify-between py-4">
          <div>
            <Text>测试通知</Text>
            <Paragraph className="text-gray-500 text-sm mb-0">
              发送一条测试通知验证功能
            </Paragraph>
          </div>
          <Button
            type="default"
            icon={<BellFilled />}
            onClick={handleTest}
            loading={isLoading}
          >
            发送测试
          </Button>
        </div>
      )}

      {isEnabled && (
        <div className="mt-4 p-3 bg-green-50 rounded-lg flex items-center gap-2">
          <CheckCircleOutlined className="text-green-500" />
          <Text className="text-green-700">推送通知已启用</Text>
        </div>
      )}
    </Card>
  );
};

export default NotificationSettings;
