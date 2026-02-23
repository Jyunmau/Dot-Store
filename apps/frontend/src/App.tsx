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
 * V2.2 仪表盘页面组件
 */
const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();

  return (
    <div className="p-4 md:p-6">
      <div className="bg-white rounded-lg shadow p-4 md:p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">欢迎使用 Dot-Store 点单收银系统</h2>
        <p className="text-gray-600">当前版本：V2.2</p>
        <p className="text-gray-600 mt-2">店铺名称：{user?.shop_name}</p>
        <p className="text-gray-600 mt-2">店铺类型：{user?.shop_type}</p>
        <p className="text-gray-600 mt-2">所在城市：{user?.city}</p>
      </div>
      
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-50 rounded-lg p-4 md:p-6">
          <h3 className="text-base font-medium text-green-900 mb-2">今日订单</h3>
          <p className="text-2xl font-bold text-green-700">0</p>
        </div>
        <div className="bg-blue-50 rounded-lg p-4 md:p-6">
          <h3 className="text-base font-medium text-blue-900 mb-2">今日收入</h3>
          <p className="text-2xl font-bold text-blue-700">¥0.00</p>
        </div>
        <div className="bg-orange-50 rounded-lg p-4 md:p-6">
          <h3 className="text-base font-medium text-orange-900 mb-2">库存预警</h3>
          <p className="text-2xl font-bold text-orange-700">0</p>
        </div>
      </div>
      
      <div className="mt-4 bg-blue-50 rounded-lg p-4 md:p-6">
        <h3 className="text-base font-medium text-blue-900 mb-2">PWA功能</h3>
        <p className="text-blue-700 text-sm">
          本应用支持PWA，您可以将其添加到主屏幕以获得更好的使用体验。
          支持离线访问历史数据，网络恢复后自动同步。
        </p>
      </div>
    </div>
  );
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
    // 初始化时检查登录状态
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
              {/* V2.2 仪表盘 */}
              <Route index element={<DashboardPage />} />
              
              {/* V2.2 记录模块 */}
              <Route path="records/orders" element={<OrderListPage />} />
              <Route path="records/transactions" element={<TransactionListPage />} />
              <Route path="records/stock" element={<IngredientListPage />} />
              
              {/* V2.2 账户模块 */}
              <Route path="accounts/customers" element={<CustomerList />} />
              <Route path="accounts/cash" element={<CashAccount />} />
              
              {/* V2.2 洞察模块 - 占位页面 */}
              <Route path="insights/income" element={<DashboardPage />} />
              <Route path="insights/cost" element={<DashboardPage />} />
              <Route path="insights/profit" element={<DashboardPage />} />
              <Route path="insights/cashflow" element={<DashboardPage />} />
              
              {/* V2.2 报表模块 */}
              <Route path="reports" element={<ReportPage />} />
              <Route path="reports/daily" element={<ReportPage />} />
              <Route path="reports/weekly" element={<ReportPage />} />
              <Route path="reports/monthly" element={<ReportPage />} />
              
              {/* V2.2 库存模块 */}
              <Route path="stock/warnings" element={<StockWarningPage />} />
              <Route path="stock/transactions" element={<StockTransactionPage />} />
              
              {/* V2.2 事件日志 */}
              <Route path="events" element={<EventLog />} />
              
              {/* V2.2 设置模块 */}
              <Route path="settings/profile" element={<DashboardPage />} />
              <Route path="settings/shop" element={<DashboardPage />} />
              <Route path="settings/notification" element={<NotificationSettingsPage />} />
              <Route path="settings/staff" element={<StaffManagementPage />} />
              
              {/* 兼容旧路由 */}
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
