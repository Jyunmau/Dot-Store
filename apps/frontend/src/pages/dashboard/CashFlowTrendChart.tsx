/**
 * Dot-Store V2.2 现金流趋势图表组件
 */
import React from 'react';
import { Card, Empty } from 'antd';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface TrendData {
  date: string;
  income: number;
  expense: number;
}

interface CashFlowTrendChartProps {
  trendData: TrendData[];
}

/**
 * 现金流趋势图表组件
 */
const CashFlowTrendChart: React.FC<CashFlowTrendChartProps> = ({ trendData }) => {
  if (!trendData || trendData.length === 0) {
    return (
      <Card title="近7天现金流趋势">
        <Empty description="暂无趋势数据" />
      </Card>
    );
  }

  const formatTooltip = (value: number) => {
    return `¥${value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`;
  };

  const formatYAxis = (value: number) => {
    if (value >= 10000) {
      return `${(value / 10000).toFixed(1)}万`;
    }
    return value.toFixed(0);
  };

  return (
    <Card title="近7天现金流趋势">
      <div style={{ height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={trendData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 10 }}
            />
            <YAxis 
              tickFormatter={formatYAxis}
              tick={{ fontSize: 10 }}
            />
            <Tooltip formatter={formatTooltip} />
            <Legend />
            <Line
              type="monotone"
              dataKey="income"
              name="收入"
              stroke="#52c41a"
              strokeWidth={2}
              dot={{ r: 3 }}
            />
            <Line
              type="monotone"
              dataKey="expense"
              name="支出"
              stroke="#ff4d4f"
              strokeWidth={2}
              dot={{ r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

export default CashFlowTrendChart;
