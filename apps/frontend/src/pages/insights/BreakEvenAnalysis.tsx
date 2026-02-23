/**
 * Dot-Store V2.2 盈亏平衡分析组件
 */
import React from 'react';
import { Card, Row, Col, Statistic, Progress, Typography, Empty, Spin, Tag, Descriptions } from 'antd';
import {
  CheckCircleOutlined,
  CloseCircleOutlined,
  MinusCircleOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import type { BreakEvenAnalysis } from '@/types/cashFlow';

const { Title, Text } = Typography;

interface BreakEvenAnalysisProps {
  data?: BreakEvenAnalysis | null;
  loading?: boolean;
}

/**
 * 盈亏平衡分析组件
 */
const BreakEvenAnalysisComponent: React.FC<BreakEvenAnalysisProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Spin size="large" />
      </div>
    );
  }

  if (!data) {
    return (
      <Empty description="暂无盈亏平衡分析数据" className="py-20" />
    );
  }

  const getStatusInfo = () => {
    switch (data.status) {
      case 'profit':
        return {
          icon: <CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a' }} />,
          text: '盈利',
          color: '#52c41a',
          bgColor: '#f6ffed',
        };
      case 'loss':
        return {
          icon: <CloseCircleOutlined style={{ fontSize: 48, color: '#f5222d' }} />,
          text: '亏损',
          color: '#f5222d',
          bgColor: '#fff2f0',
        };
      case 'break_even':
        return {
          icon: <MinusCircleOutlined style={{ fontSize: 48, color: '#faad14' }} />,
          text: '盈亏平衡',
          color: '#faad14',
          bgColor: '#fffbe6',
        };
      default:
        return {
          icon: null,
          text: '未知',
          color: '#d9d9d9',
          bgColor: '#fafafa',
        };
    }
  };

  const statusInfo = getStatusInfo();

  const safetyMarginPercent = Math.min(100, Math.max(0, data.safety_margin_ratio));

  return (
    <Row gutter={[24, 24]}>
      <Col xs={24} lg={8}>
        <Card className="h-full text-center" styles={{ body: { padding: '24px' } }}>
          <div
            className="py-6 rounded-lg mb-4"
            style={{ backgroundColor: statusInfo.bgColor }}
          >
            {statusInfo.icon}
            <Title level={3} style={{ color: statusInfo.color, marginTop: 16, marginBottom: 0 }}>
              {statusInfo.text}
            </Title>
          </div>
          
          <Progress
            type="dashboard"
            percent={safetyMarginPercent}
            strokeColor={statusInfo.color}
            format={(percent) => (
              <span style={{ color: statusInfo.color }}>
                {percent?.toFixed(0)}%
              </span>
            )}
          />
          <Text type="secondary">安全边际率</Text>
        </Card>
      </Col>

      <Col xs={24} lg={16}>
        <Card className="h-full">
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12}>
              <Statistic
                title="盈亏平衡点"
                value={Number(data.break_even_point)}
                precision={2}
                prefix="¥"
                valueStyle={{ fontSize: 24 }}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Statistic
                title="当前收入"
                value={Number(data.current_revenue)}
                precision={2}
                prefix="¥"
                valueStyle={{ fontSize: 24, color: '#52c41a' }}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Statistic
                title="固定成本"
                value={Number(data.fixed_cost)}
                precision={2}
                prefix="¥"
                valueStyle={{ fontSize: 20 }}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Statistic
                title="变动成本比率"
                value={data.variable_cost_ratio}
                precision={1}
                suffix="%"
                valueStyle={{ fontSize: 20 }}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Statistic
                title="边际贡献率"
                value={data.contribution_margin_ratio}
                precision={1}
                suffix="%"
                valueStyle={{ fontSize: 20 }}
              />
            </Col>
            <Col xs={24} sm={12}>
              <Statistic
                title="安全边际"
                value={Number(data.safety_margin)}
                precision={2}
                prefix="¥"
                valueStyle={{
                  fontSize: 20,
                  color: data.safety_margin >= 0 ? '#52c41a' : '#f5222d',
                }}
                prefix={data.safety_margin >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
              />
            </Col>
          </Row>

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <Title level={5} className="mb-3">分析说明</Title>
            <Descriptions column={1} size="small">
              <Descriptions.Item label="盈亏平衡点">
                当销售额达到 ¥{Number(data.break_even_point).toLocaleString('zh-CN', { minimumFractionDigits: 2 })} 时，
                收支相抵，不盈不亏
              </Descriptions.Item>
              <Descriptions.Item label="当前状态">
                {data.status === 'profit' && `当前盈利，超出盈亏平衡点 ¥${Number(data.safety_margin).toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`}
                {data.status === 'loss' && `当前亏损，距离盈亏平衡点还差 ¥${Math.abs(Number(data.safety_margin)).toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`}
                {data.status === 'break_even' && '当前刚好达到盈亏平衡点'}
              </Descriptions.Item>
              <Descriptions.Item label="建议">
                {data.status === 'profit' && '经营状况良好，可考虑扩大经营规模'}
                {data.status === 'loss' && '建议优化成本结构，增加收入来源'}
                {data.status === 'break_even' && '建议关注经营效率，提高盈利能力'}
              </Descriptions.Item>
            </Descriptions>
          </div>
        </Card>
      </Col>
    </Row>
  );
};

export default BreakEvenAnalysisComponent;
