/**
 * Dot-Store V2.2 支出结构图表组件
 */
import React from 'react';
import { Card, Row, Col, List, Typography, Empty, Spin, Statistic, Tag, Alert } from 'antd';
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
import { WarningOutlined } from '@ant-design/icons';
import type { ExpenseStructureResponse } from '@/types/cashFlow';

const { Text, Title } = Typography;

interface ExpenseStructureChartProps {
  data?: ExpenseStructureResponse | null;
  loading?: boolean;
}

const COLORS = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#eb2f96', '#722ed1'];

/**
 * 支出结构图表组件
 */
const ExpenseStructureChart: React.FC<ExpenseStructureChartProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Spin size="large" />
      </div>
    );
  }

  if (!data) {
    return (
      <Empty description="暂无支出数据" className="py-20" />
    );
  }

  const categoryData = Object.entries(data.expense_by_category || {}).map(([name, value]) => ({
    name,
    value: Number(value),
    percentage: data.total_expense > 0 ? (Number(value) / Number(data.total_expense)) * 100 : 0,
  }));

  const behaviorData = Object.entries(data.expense_by_behavior || {}).map(([name, value]) => ({
    name: name === 'fixed' ? '固定成本' : name === 'variable' ? '变动成本' : name,
    value: Number(value),
  }));

  const functionData = Object.entries(data.expense_by_function || {}).map(([name, value]) => ({
    name,
    value: Number(value),
  }));

  const trendData = (data.expense_trend || []).map((item) => ({
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
    <div>
      {data.anomaly_detected && (
        <Alert
          message="检测到支出异常"
          description="近期支出存在异常波动，请关注支出情况"
          type="warning"
          showIcon
          icon={<WarningOutlined />}
          className="mb-4"
        />
      )}

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={12}>
          <Card title="支出分类占比" className="h-full">
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
              title="总支出"
              value={Number(data.total_expense)}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#f5222d', fontSize: 28 }}
              className="mb-4"
            />

            <Row gutter={16} className="mb-4">
              <Col span={12}>
                <Title level={5}>成本行为</Title>
                {behaviorData.length > 0 ? (
                  <List
                    size="small"
                    dataSource={behaviorData}
                    renderItem={(item) => (
                      <List.Item>
                        <div className="flex justify-between w-full">
                          <Text>{item.name}</Text>
                          <Text strong>¥{item.value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}</Text>
                        </div>
                      </List.Item>
                    )}
                  />
                ) : (
                  <Empty description="暂无数据" image={Empty.PRESENTED_IMAGE_SIMPLE} />
                )}
              </Col>
              <Col span={12}>
                <Title level={5}>成本功能</Title>
                {functionData.length > 0 ? (
                  <List
                    size="small"
                    dataSource={functionData}
                    renderItem={(item) => (
                      <List.Item>
                        <div className="flex justify-between w-full">
                          <Text>{item.name}</Text>
                          <Text strong>¥{item.value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}</Text>
                        </div>
                      </List.Item>
                    )}
                  />
                ) : (
                  <Empty description="暂无数据" image={Empty.PRESENTED_IMAGE_SIMPLE} />
                )}
              </Col>
            </Row>

            <Title level={5} className="mb-3">支出趋势</Title>
            {trendData.length > 0 ? (
              <div style={{ height: 150 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} />
                    <Tooltip formatter={formatTooltip} />
                    <Line
                      type="monotone"
                      dataKey="amount"
                      stroke="#f5222d"
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
    </div>
  );
};

export default ExpenseStructureChart;
