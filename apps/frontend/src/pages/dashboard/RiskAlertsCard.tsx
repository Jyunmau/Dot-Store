/**
 * Dot-Store V2.2 风险预警卡片组件
 */
import React from 'react';
import { Card, List, Tag, Button, Empty, Typography, Space } from 'antd';
import { 
  AlertOutlined, 
  CheckCircleOutlined,
  WarningOutlined,
  CloseCircleOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons';
import type { RiskAlert } from '@/types/cashFlow';

const { Text } = Typography;

interface RiskAlertsCardProps {
  alerts: RiskAlert[];
  onResolve?: (alertId: number) => void;
}

/**
 * 风险预警卡片组件
 */
const RiskAlertsCard: React.FC<RiskAlertsCardProps> = ({ alerts, onResolve }) => {
  const getAlertIcon = (level: string) => {
    switch (level) {
      case 'critical':
        return <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: 20 }} />;
      case 'high':
        return <AlertOutlined style={{ color: '#ff7875', fontSize: 20 }} />;
      case 'medium':
        return <WarningOutlined style={{ color: '#faad14', fontSize: 20 }} />;
      case 'low':
        return <InfoCircleOutlined style={{ color: '#52c41a', fontSize: 20 }} />;
      default:
        return <InfoCircleOutlined style={{ color: '#1890ff', fontSize: 20 }} />;
    }
  };

  const getAlertTag = (level: string) => {
    const config: Record<string, { color: string; text: string }> = {
      critical: { color: 'red', text: '严重' },
      high: { color: 'orange', text: '高' },
      medium: { color: 'gold', text: '中' },
      low: { color: 'green', text: '低' },
    };
    const { color, text } = config[level] || { color: 'default', text: level };
    return <Tag color={color}>{text}</Tag>;
  };

  const getBgColor = (level: string) => {
    switch (level) {
      case 'critical':
      case 'high':
        return '#fff2f0';
      case 'medium':
        return '#fffbe6';
      case 'low':
        return '#f6ffed';
      default:
        return '#fafafa';
    }
  };

  if (alerts.length === 0) {
    return (
      <Card title="风险预警" className="h-full">
        <Empty
          image={<CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a' }} />}
          description={
            <Text type="success">暂无风险预警，经营状况良好</Text>
          }
        />
      </Card>
    );
  }

  return (
    <Card 
      title={
        <Space>
          <AlertOutlined style={{ color: '#ff4d4f' }} />
          <span>风险预警</span>
          <Tag color="red">{alerts.length}</Tag>
        </Space>
      }
      className="h-full"
    >
      <List
        dataSource={alerts}
        renderItem={(alert) => (
          <List.Item
            style={{ 
              backgroundColor: getBgColor(alert.alert_level),
              padding: 12,
              borderRadius: 8,
              marginBottom: 8,
            }}
          >
            <List.Item.Meta
              avatar={getAlertIcon(alert.alert_level)}
              title={
                <Space>
                  {getAlertTag(alert.alert_level)}
                  <Text strong>{alert.message}</Text>
                </Space>
              }
              description={
                <div className="mt-2">
                  {alert.suggestions && alert.suggestions.length > 0 && (
                    <div className="mb-2">
                      <Text type="secondary" className="block mb-1">建议措施：</Text>
                      <ul className="list-disc list-inside text-gray-600 text-sm">
                        {alert.suggestions.map((suggestion, index) => (
                          <li key={index}>{suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <Text type="secondary" className="text-xs">
                    {alert.alert_date}
                  </Text>
                </div>
              }
            />
            {onResolve && (
              <Button
                type="link"
                size="small"
                icon={<CheckCircleOutlined />}
                onClick={() => onResolve(alert.id)}
              >
                已处理
              </Button>
            )}
          </List.Item>
        )}
      />
    </Card>
  );
};

export default RiskAlertsCard;
