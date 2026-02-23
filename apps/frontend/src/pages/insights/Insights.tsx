/**
 * Dot-Store V2.2 洞察页面
 */
import React, { useState, useEffect } from 'react';
import { Card, Tabs, Typography, DatePicker, Button, Space, message } from 'antd';
import { BulbOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { useCashFlowStore } from '@/store/cashFlowStore';
import IncomeStructureChart from './IncomeStructureChart';
import ExpenseStructureChart from './ExpenseStructureChart';
import BreakEvenAnalysis from './BreakEvenAnalysis';
import CashFlowForecastChart from './CashFlowForecastChart';

const { Title } = Typography;
const { RangePicker } = DatePicker;

/**
 * 洞察页面组件
 */
const Insights: React.FC = () => {
  const [activeTab, setActiveTab] = useState('income');
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().startOf('month'),
    dayjs().endOf('month'),
  ]);

  const {
    incomeStructure,
    expenseStructure,
    breakEvenAnalysis,
    forecastData,
    loading,
    error,
    fetchIncomeStructure,
    fetchExpenseStructure,
    fetchBreakEvenAnalysis,
    fetchForecast,
  } = useCashFlowStore();

  useEffect(() => {
    if (error) {
      message.error(error);
    }
  }, [error]);

  useEffect(() => {
    const [start, end] = dateRange;
    fetchIncomeStructure(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
    fetchExpenseStructure(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
    fetchBreakEvenAnalysis();
    fetchForecast(30);
  }, [dateRange, fetchIncomeStructure, fetchExpenseStructure, fetchBreakEvenAnalysis, fetchForecast]);

  const handleDateRangeChange = (dates: [dayjs.Dayjs | null, dayjs.Dayjs | null] | null) => {
    if (dates && dates[0] && dates[1]) {
      setDateRange([dates[0], dates[1]]);
    }
  };

  const handleRefresh = () => {
    const [start, end] = dateRange;
    fetchIncomeStructure(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
    fetchExpenseStructure(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
    fetchBreakEvenAnalysis();
    fetchForecast(30);
  };

  const tabItems = [
    {
      key: 'income',
      label: '收入结构',
      children: (
        <IncomeStructureChart
          data={incomeStructure}
          loading={loading}
        />
      ),
    },
    {
      key: 'expense',
      label: '成本结构',
      children: (
        <ExpenseStructureChart
          data={expenseStructure}
          loading={loading}
        />
      ),
    },
    {
      key: 'breakeven',
      label: '盈亏平衡',
      children: (
        <BreakEvenAnalysis
          data={breakEvenAnalysis}
          loading={loading}
        />
      ),
    },
    {
      key: 'forecast',
      label: '现金流预测',
      children: (
        <CashFlowForecastChart
          data={forecastData}
          loading={loading}
        />
      ),
    },
  ];

  return (
    <div className="p-4 md:p-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <Title level={3} className="mb-4 md:mb-0">
          <BulbOutlined className="mr-2" />
          经营洞察
        </Title>
        <Space>
          <RangePicker
            value={dateRange}
            onChange={handleDateRangeChange}
            format="YYYY-MM-DD"
            placeholder={['开始日期', '结束日期']}
          />
          <Button type="primary" onClick={handleRefresh} loading={loading}>
            刷新数据
          </Button>
        </Space>
      </div>

      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={tabItems}
          size="large"
        />
      </Card>
    </div>
  );
};

export default Insights;
