/**
 * Dot-Store V2.2 收入结构图表组件
 */
import React from 'react';
import { Card, Row, Col, List, Typography, Empty, Spin, Statistic, Tag } from 'antd';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import type { IncomeStructureResponse } from '@/types/cashFlow';

const { Text, Title } = Typography;

interface IncomeStructureChartProps {
  data?: IncomeStructureResponse | null;
  loading?: boolean;
}

const COLORS = ['#52c41a', '#1890ff', '#722ed1', '#fa8c16', '#eb2f96', '#13c2c2'];

/**
 * 收入结构图表组件
 */
const IncomeStructureChart: React.FC<IncomeStructureChartProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Spin size="large" />
      </div>
    );
  }

  if (!data) {
    return (
      <Empty description="暂无收入数据" className="py-20" />
    );
  }

  const categoryData = Object.entries(data.income_by_category || {}).map(([name, value]) => ({
    name,
    value: Number(value),
    percentage: data.total_income > 0 ? (Number(value) / Number(data.total_income)) * 100 : 0,
  }));

  const modeData = Object.entries(data.income_by_mode || {}).map(([name, value]) => ({
    name,
    value: Number(value),
  }));

  const trendData = (data.income_trend || []).map((item) => ({
    date: item.date,
    amount: Number(item.amount),
  }));

  const formatTooltip = (value: number) => {
    return `¥${value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`;
  };

  const renderCustomizedLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
  }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    if (percent < 0.05) return null;

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor="middle"
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <Row gutter={[24, 24]}>
      <Col xs={24} lg={12}>
        <Card title="收入分类占比" className="h-full">
          {categoryData.length > 0 ? (
            <>
              <div style={{ height: 280 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={renderCustomizedLabel}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {categoryData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={formatTooltip} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              <List
                dataSource={categoryData}
                renderItem={(item, index) => (
                  <List.Item>
                    <div className="flex items-center justify-between w-full">
                      <div className="flex items-center">
                        <div
                          className="w-3 h-3 rounded-full mr-2"
                          style={{ backgroundColor: COLORS[index % COLORS.length] }}
                        />
                        <Text>{item.name}</Text>
                      </div>
                      <div className="text-right">
                        <Text strong className="block">
                          ¥{item.value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}
                        </Text>
                        <Text type="secondary" className="text-xs">
                          {item.percentage.toFixed(1)}%
                        </Text>
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            </>
          ) : (
            <Empty description="暂无分类数据" />
          )}
        </Card>
      </Col>

      <Col xs={24} lg={12}>
        <Card className="h-full">
          <Statistic
            title="总收入"
            value={Number(data.total_income)}
            precision={2}
            prefix="¥"
            valueStyle={{ color: '#52c41a', fontSize: 28 }}
            className="mb-4"
          />
          
          <Row gutter={16} className="mb-4">
            <Col span={12}>
              <Statistic
                title="稳定性评分"
                value={data.stability_score}
                precision={1}
                suffix="分"
                valueStyle={{ fontSize: 18 }}
              />
            </Col>
            <Col span={12}>
              <Statistic
                title="增长率"
                value={data.growth_rate || 0}
                precision={1}
                suffix="%"
                valueStyle={{
                  color: (data.growth_rate || 0) >= 0 ? '#52c41a' : '#f5222d',
                  fontSize: 18,
                }}
                prefix={(data.growth_rate || 0) >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
              />
            </Col>
          </Row>

          <Title level={5} className="mb-3">收入趋势</Title>
          {trendData.length > 0 ? (
            <div style={{ height: 200 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip formatter={formatTooltip} />
                  <Line
                    type="monotone"
                    dataKey="amount"
                    stroke="#52c41a"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <Empty description="暂无趋势数据" />
          )}
        </Card>
      </Col>
    </Row>
  );
};

export default IncomeStructureChart;
