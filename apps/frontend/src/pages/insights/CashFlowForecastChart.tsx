/**
 * Dot-Store V2.2 现金流预测图表组件
 */
import React from 'react';
import { Card, Row, Col, Typography, Empty, Spin, Statistic, Alert, Table, Tag } from 'antd';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import type { CashFlowForecastListResponse } from '@/types/cashFlow';

const { Text } = Typography;

interface CashFlowForecastChartProps {
  data?: CashFlowForecastListResponse | null;
  loading?: boolean;
}

/**
 * 现金流预测图表组件
 */
const CashFlowForecastChart: React.FC<CashFlowForecastChartProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Spin size="large" />
      </div>
    );
  }

  if (!data || !data.items || data.items.length === 0) {
    return (
      <Empty description="暂无预测数据" className="py-20" />
    );
  }

  const chartData = data.items.map((item) => ({
    date: item.target_date.slice(5),
    fullDate: item.target_date,
    predicted_balance: item.predicted_balance,
    predicted_income: item.predicted_income,
    predicted_expense: item.predicted_expense,
    confidence: item.confidence_level,
    risk_alert: item.risk_alert,
  }));

  const riskAlerts = data.items.filter((item) => item.risk_alert);

  const formatYAxis = (value: number) => {
    if (value >= 10000) {
      return `${(value / 10000).toFixed(1)}万`;
    }
    return value.toFixed(0);
  };

  const formatTooltip = (value: number) => {
    return `¥${value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`;
  };

  const minBalance = Math.min(...chartData.map((d) => d.predicted_balance));
  const maxBalance = Math.max(...chartData.map((d) => d.predicted_balance));

  const columns = [
    {
      title: '日期',
      dataIndex: 'target_date',
      key: 'target_date',
      render: (date: string) => date.slice(5),
    },
    {
      title: '预测收入',
      dataIndex: 'predicted_income',
      key: 'predicted_income',
      render: (v: number) => `¥${v.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`,
    },
    {
      title: '预测支出',
      dataIndex: 'predicted_expense',
      key: 'predicted_expense',
      render: (v: number) => `¥${v.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`,
    },
    {
      title: '预测余额',
      dataIndex: 'predicted_balance',
      key: 'predicted_balance',
      render: (v: number, record: any) => (
        <Text type={record.risk_alert ? 'danger' : undefined}>
          ¥{v.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}
        </Text>
      ),
    },
    {
      title: '置信度',
      dataIndex: 'confidence_level',
      key: 'confidence_level',
      render: (v: number) => `${v.toFixed(0)}%`,
    },
    {
      title: '状态',
      dataIndex: 'risk_alert',
      key: 'risk_alert',
      render: (alert: boolean) => 
        alert ? <Tag color="red">风险</Tag> : <Tag color="green">正常</Tag>,
    },
  ];

  return (
    <div>
      {riskAlerts.length > 0 && (
        <Alert
          message="现金流风险预警"
          description={`未来${riskAlerts.length}天可能出现资金缺口，建议提前做好资金安排。`}
          type="warning"
          showIcon
          className="mb-4"
        />
      )}

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <Card title="未来90天现金流预测" styles={{ body: { padding: '16px' } }}>
            <div style={{ height: 350 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={chartData}
                  margin={{
                    top: 10,
                    right: 30,
                    left: 0,
                    bottom: 0,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tick={{ fontSize: 10 }}
                    interval="preserveStartEnd"
                  />
                  <YAxis 
                    tickFormatter={formatYAxis}
                    tick={{ fontSize: 10 }}
                  />
                  <Tooltip
                    formatter={formatTooltip}
                    labelFormatter={(label) => `日期: ${label}`}
                  />
                  <ReferenceLine y={0} stroke="#ff4d4f" strokeDasharray="3 3" />
                  <Area
                    type="monotone"
                    dataKey="predicted_balance"
                    name="预测余额"
                    stroke="#1890ff"
                    fill="#1890ff"
                    fillOpacity={0.3}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card styles={{ body: { padding: '16px' } }}>
            <Statistic
              title="当前余额"
              value={data.current_balance}
              precision={2}
              prefix="¥"
              valueStyle={{ fontSize: 24 }}
              className="mb-4"
            />
            <Statistic
              title="预测最低余额"
              value={minBalance}
              precision={2}
              prefix="¥"
              valueStyle={{ 
                fontSize: 20,
                color: minBalance < 0 ? '#ff4d4f' : '#52c41a'
              }}
              className="mb-4"
            />
            <Statistic
              title="预测最高余额"
              value={maxBalance}
              precision={2}
              prefix="¥"
              valueStyle={{ fontSize: 20 }}
              className="mb-4"
            />
            <Statistic
              title="风险预警天数"
              value={riskAlerts.length}
              suffix="天"
              valueStyle={{ 
                fontSize: 20,
                color: riskAlerts.length > 0 ? '#ff4d4f' : '#52c41a'
              }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="预测明细（未来30天）" className="mt-4">
        <Table
          dataSource={data.items.slice(0, 30)}
          columns={columns}
          rowKey="id"
          pagination={false}
          size="small"
          scroll={{ x: 'max-content' }}
        />
      </Card>
    </div>
  );
};

export default CashFlowForecastChart;
