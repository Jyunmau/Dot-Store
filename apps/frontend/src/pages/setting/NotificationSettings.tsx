/**
 * 通知设置页面
 */
import React from 'react';
import { Card, Typography } from 'antd';
import { BellOutlined } from '@ant-design/icons';
import NotificationSettings from '@/components/PWA/NotificationSettings';

const { Title } = Typography;

const NotificationSettingsPage: React.FC = () => {
  return (
    <div className="p-6">
      <Card>
        <div className="flex items-center mb-4">
          <BellOutlined className="text-xl mr-2" />
          <Title level={4} className="m-0">通知设置</Title>
        </div>
        <NotificationSettings />
      </Card>
    </div>
  );
};

export default NotificationSettingsPage;
