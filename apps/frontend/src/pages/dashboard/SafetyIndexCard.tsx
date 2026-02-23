/**
 * Dot-Store V2.2 安全指数卡片组件
 */
import React from 'react';
import { Card, Progress, Typography, Descriptions, Empty } from 'antd';
import { SafetyCertificateOutlined, WarningOutlined, CloseCircleOutlined } from '@ant-design/icons';
import type { SafetyIndex } from '@/types/cashFlow';

const { Text } = Typography;

interface SafetyIndexCardProps {
  safetyIndex?: SafetyIndex | null;
}

/**
 * 安全指数卡片组件
 */
const SafetyIndexCard: React.FC<SafetyIndexCardProps> = ({ safetyIndex }) => {
  if (!safetyIndex) {
    return (
      <Card title="安全指数" className="h-full">
        <Empty description="暂无数据" />
      </Card>
    );
  }

  const getIcon = () => {
    switch (safetyIndex.safety_level) {
      case 'safe':
        return <SafetyCertificateOutlined style={{ fontSize: 48, color: safetyIndex.color_code }} />;
      case 'warning':
        return <WarningOutlined style={{ fontSize: 48, color: safetyIndex.color_code }} />;
      case 'danger':
        return <CloseCircleOutlined style={{ fontSize: 48, color: safetyIndex.color_code }} />;
      default:
        return null;
    }
  };

  const getBgColor = () => {
    switch (safetyIndex.safety_level) {
      case 'safe':
        return '#f6ffed';
      case 'warning':
        return '#fffbe6';
      case 'danger':
        return '#fff2f0';
      default:
        return '#f5f5f5';
    }
  };

  return (
    <Card 
      title="现金流安全指数" 
      className="h-full"
      styles={{
        body: { padding: '16px' }
      }}
    >
      <div 
        className="text-center py-4 rounded-lg mb-4"
        style={{ backgroundColor: getBgColor() }}
      >
        {getIcon()}
        <div className="mt-2">
          <Progress
            type="circle"
            percent={safetyIndex.safety_score}
            strokeColor={safetyIndex.color_code}
            format={(percent) => (
              <span style={{ color: safetyIndex.color_code, fontWeight: 'bold' }}>
                {percent?.toFixed(0)}
              </span>
            )}
            size={80}
          />
        </div>
        <Text 
          strong 
          style={{ color: safetyIndex.color_code, fontSize: 16 }}
        >
          {safetyIndex.message}
        </Text>
      </div>

      <Descriptions column={1} size="small">
        <Descriptions.Item label="现金余额">
          ¥{safetyIndex.factors.cash_balance.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}
        </Descriptions.Item>
        <Descriptions.Item label="预收款负债">
          ¥{safetyIndex.factors.liability.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}
        </Descriptions.Item>
        <Descriptions.Item label="可用净现金">
          ¥{safetyIndex.factors.net_available.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}
        </Descriptions.Item>
        <Descriptions.Item label="可运营天数">
          {safetyIndex.factors.days_of_operation} 天
        </Descriptions.Item>
      </Descriptions>
    </Card>
  );
};

export default SafetyIndexCard;
