/**
 * Dot-Store V2.2 现金流概览卡片组件
 */
import React from 'react';
import { Card, Row, Col, Statistic, Typography, Divider, Alert } from 'antd';
import {
  WalletOutlined,
  RiseOutlined,
  FallOutlined,
  DollarOutlined,
  WarningOutlined,
} from '@ant-design/icons';

const { Text, Title } = Typography;

interface ForecastSummary {
  has_risk: boolean;
  predicted_balance_end: number;
  avg_daily_income: number;
  avg_daily_expense: number;
}

interface CashFlowOverviewCardProps {
  currentBalance?: number;
  yesterdayChange?: number;
  monthlyIncome?: number;
  monthlyExpense?: number;
  monthlyProfit?: number;
  forecastSummary?: ForecastSummary;
}

/**
 * 现金流概览卡片组件
 */
const CashFlowOverviewCard: React.FC<CashFlowOverviewCardProps> = ({
  currentBalance = 0,
  yesterdayChange = 0,
  monthlyIncome = 0,
  monthlyExpense = 0,
  monthlyProfit = 0,
  forecastSummary,
}) => {
  return (
    <Card title="现金流概览" className="h-full">
      {forecastSummary?.has_risk && (
        <Alert
          message="未来7天存在资金风险"
          description="根据预测，未来可能出现资金缺口，建议提前做好资金安排"
          type="warning"
          showIcon
          icon={<WarningOutlined />}
          className="mb-4"
        />
      )}

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Card 
            className="bg-blue-50"
            styles={{ body: { padding: '16px' } }}
          >
            <Statistic
              title={<Text strong>当前余额</Text>}
              value={Number(currentBalance)}
              precision={2}
              prefix={<WalletOutlined />}
              suffix="元"
              valueStyle={{ color: '#1890ff', fontSize: 24 }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={12}>
          <Card 
            className={yesterdayChange >= 0 ? 'bg-green-50' : 'bg-red-50'}
            styles={{ body: { padding: '16px' } }}
          >
            <Statistic
              title={<Text strong>昨日变动</Text>}
              value={Number(yesterdayChange)}
              precision={2}
              prefix={yesterdayChange >= 0 ? <RiseOutlined /> : <FallOutlined />}
              suffix="元"
              valueStyle={{ 
                color: yesterdayChange >= 0 ? '#52c41a' : '#ff4d4f',
                fontSize: 24 
              }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={8}>
          <Card 
            className="bg-green-50"
            styles={{ body: { padding: '12px' } }}
          >
            <Statistic
              title={<Text type="secondary">本月收入</Text>}
              value={Number(monthlyIncome)}
              precision={2}
              prefix={<RiseOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a', fontSize: 18 }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={8}>
          <Card 
            className="bg-orange-50"
            styles={{ body: { padding: '12px' } }}
          >
            <Statistic
              title={<Text type="secondary">本月支出</Text>}
              value={Number(monthlyExpense)}
              precision={2}
              prefix={<FallOutlined style={{ color: '#fa8c16' }} />}
              valueStyle={{ color: '#fa8c16', fontSize: 18 }}
            />
          </Card>
        </Col>

        <Col xs={24} sm={8}>
          <Card 
            className={monthlyProfit >= 0 ? 'bg-blue-50' : 'bg-red-50'}
            styles={{ body: { padding: '12px' } }}
          >
            <Statistic
              title={<Text type="secondary">本月利润</Text>}
              value={Number(monthlyProfit)}
              precision={2}
              prefix={<DollarOutlined />}
              valueStyle={{ 
                color: monthlyProfit >= 0 ? '#1890ff' : '#ff4d4f',
                fontSize: 18 
              }}
            />
          </Card>
        </Col>
      </Row>

      {forecastSummary && (
        <>
          <Divider />
          <Title level={5} className="mb-3">预测摘要（未来7天）</Title>
          <Row gutter={16}>
            <Col span={8}>
              <Statistic
                title="日均预测收入"
                value={forecastSummary.avg_daily_income}
                precision={2}
                prefix="¥"
                valueStyle={{ fontSize: 14 }}
              />
            </Col>
            <Col span={8}>
              <Statistic
                title="日均预测支出"
                value={forecastSummary.avg_daily_expense}
                precision={2}
                prefix="¥"
                valueStyle={{ fontSize: 14 }}
              />
            </Col>
            <Col span={8}>
              <Statistic
                title="预测期末余额"
                value={forecastSummary.predicted_balance_end}
                precision={2}
                prefix="¥"
                valueStyle={{ 
                  fontSize: 14,
                  color: forecastSummary.predicted_balance_end >= 0 ? '#52c41a' : '#ff4d4f'
                }}
              />
            </Col>
          </Row>
        </>
      )}
    </Card>
  );
};

export default CashFlowOverviewCard;
