/**
 * Dot-Store V2.2 应用主组件
 */
import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, App as AntApp } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { useAuthStore } from '@/store/authStore';
import { LoginPage, RegisterPage } from '@/pages/auth';
import { StaffManagementPage, NotificationSettingsPage } from '@/pages/setting';
import { OrderListPage, OrderRecyclePage, CategoryManagePage, TagManagePage } from '@/pages/order';
import { TransactionListPage, TransactionCategoryManagePage } from '@/pages/transaction';
import { ReportPage } from '@/pages/report';
import { IngredientListPage, StockRecordPage, StockWarningPage } from '@/pages/stock';
import { MemberListPage, PointsRecordPage, PointsExchangePage } from '@/pages/member';
import { BackupManagePage, BackupSettingsPage } from '@/pages/backup';
import { MainLayout } from '@/components/Layout';
import { OfflineIndicator, PWAInstallPrompt } from '@/components/PWA';
import { EventLog } from '@/pages/event';
import { CustomerList } from '@/pages/customer';
import { CashAccount } from '@/pages/cash';
import { Dashboard } from '@/pages/dashboard';
import { Insights } from '@/pages/insights';

/**
 * 受保护的路由组件
 */
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

/**
 * 库存流水页面组件
 */
const StockTransactionPage: React.FC = () => {
  return (
    <div className="p-4 md:p-6">
      <div className="bg-white rounded-lg shadow p-4 md:p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">库存流水</h2>
        <p className="text-gray-600">V2.2新增功能 - 库存流水管理</p>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const { token } = useAuthStore();

  useEffect(() => {
  }, [token]);

  return (
    <ConfigProvider locale={zhCN}>
      <AntApp>
        <BrowserRouter>
          <OfflineIndicator />
          <PWAInstallPrompt />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <MainLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Dashboard />} />
              
              <Route path="records/orders" element={<OrderListPage />} />
              <Route path="records/transactions" element={<TransactionListPage />} />
              <Route path="records/stock" element={<IngredientListPage />} />
              
              <Route path="accounts/customers" element={<CustomerList />} />
              <Route path="accounts/cash" element={<CashAccount />} />
              
              <Route path="insights" element={<Insights />} />
              <Route path="insights/income" element={<Insights />} />
              <Route path="insights/cost" element={<Insights />} />
              <Route path="insights/profit" element={<Insights />} />
              <Route path="insights/cashflow" element={<Insights />} />
              
              <Route path="reports" element={<ReportPage />} />
              <Route path="reports/daily" element={<ReportPage />} />
              <Route path="reports/weekly" element={<ReportPage />} />
              <Route path="reports/monthly" element={<ReportPage />} />
              
              <Route path="stock/warnings" element={<StockWarningPage />} />
              <Route path="stock/transactions" element={<StockTransactionPage />} />
              
              <Route path="events" element={<EventLog />} />
              
              <Route path="settings/profile" element={<Dashboard />} />
              <Route path="settings/shop" element={<Dashboard />} />
              <Route path="settings/notification" element={<NotificationSettingsPage />} />
              <Route path="settings/staff" element={<StaffManagementPage />} />
              
              <Route path="orders" element={<Navigate to="/records/orders" replace />} />
              <Route path="orders/recycle" element={<OrderRecyclePage />} />
              <Route path="orders/categories" element={<CategoryManagePage />} />
              <Route path="orders/tags" element={<TagManagePage />} />
              <Route path="transactions" element={<Navigate to="/records/transactions" replace />} />
              <Route path="transactions/categories" element={<TransactionCategoryManagePage />} />
              <Route path="stock/ingredients" element={<Navigate to="/records/stock" replace />} />
              <Route path="stock/records" element={<StockRecordPage />} />
              <Route path="members" element={<MemberListPage />} />
              <Route path="members/points" element={<PointsRecordPage />} />
              <Route path="members/exchange" element={<PointsExchangePage />} />
              <Route path="backup" element={<BackupManagePage />} />
              <Route path="backup/settings" element={<BackupSettingsPage />} />
              <Route path="setting/staff" element={<Navigate to="/settings/staff" replace />} />
              <Route path="setting/notification" element={<Navigate to="/settings/notification" replace />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AntApp>
    </ConfigProvider>
  );
};

export default App;
