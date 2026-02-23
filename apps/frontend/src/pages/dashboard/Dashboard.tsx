/**
 * Dot-Store V2.2 仪表盘页面
 */
import React, { useEffect } from 'react';
import { Row, Col, Spin, Typography, message } from 'antd';
import { DashboardOutlined } from '@ant-design/icons';
import { useCashFlowStore } from '@/store/cashFlowStore';
import SafetyIndexCard from './SafetyIndexCard';
import CashFlowOverviewCard from './CashFlowOverviewCard';
import RiskAlertsCard from './RiskAlertsCard';
import CashFlowTrendChart from './CashFlowTrendChart';

const { Title } = Typography;

/**
 * 仪表盘页面组件
 */
const Dashboard: React.FC = () => {
  const { dashboardData, loading, error, fetchDashboard } = useCashFlowStore();

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  useEffect(() => {
    if (error) {
      message.error(error);
    }
  }, [error]);

  if (loading && !dashboardData) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6">
      <Title level={3} className="mb-6">
        <DashboardOutlined className="mr-2" />
        现金流仪表盘
      </Title>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <SafetyIndexCard safetyIndex={dashboardData?.safety_index} />
        </Col>

        <Col xs={24} lg={16}>
          <CashFlowOverviewCard
            currentBalance={dashboardData?.current_balance}
            yesterdayChange={dashboardData?.yesterday_change}
            monthlyIncome={dashboardData?.monthly_income}
            monthlyExpense={dashboardData?.monthly_expense}
            monthlyProfit={dashboardData?.monthly_profit}
            forecastSummary={dashboardData?.forecast_summary}
          />
        </Col>

        <Col xs={24}>
          <CashFlowTrendChart trendData={dashboardData?.recent_trend || []} />
        </Col>

        <Col xs={24}>
          <RiskAlertsCard alerts={dashboardData?.active_alerts || []} />
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
