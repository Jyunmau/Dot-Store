/**
 * 应用主组件
 */
import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, App as AntApp } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { useAuthStore } from '@/store/authStore';
import { LoginPage, RegisterPage } from '@/pages/auth';
import { StaffManagementPage } from '@/pages/setting';
import { OrderListPage, OrderRecyclePage, CategoryManagePage, TagManagePage } from '@/pages/order';
import { TransactionListPage, TransactionCategoryManagePage } from '@/pages/transaction';
import { ReportPage } from '@/pages/report';
import { IngredientListPage, StockRecordPage, StockWarningPage } from '@/pages/stock';
import { MemberListPage, PointsRecordPage, PointsExchangePage } from '@/pages/member';
import { BackupManagePage, BackupSettingsPage } from '@/pages/backup';
import { MainLayout } from '@/components/Layout';

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
 * 首页组件
 */
const HomePage: React.FC = () => {
  const { user } = useAuthStore();

  return (
    <div className="p-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">欢迎使用 Dot-Store 点单收银系统</h2>
        <p className="text-gray-600">当前版本：V2.1</p>
        <p className="text-gray-600 mt-2">店铺名称：{user?.shop_name}</p>
        <p className="text-gray-600 mt-2">店铺类型：{user?.shop_type}</p>
        <p className="text-gray-600 mt-2">所在城市：{user?.city}</p>
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
              <Route index element={<HomePage />} />
              <Route path="orders" element={<OrderListPage />} />
              <Route path="orders/recycle" element={<OrderRecyclePage />} />
              <Route path="orders/categories" element={<CategoryManagePage />} />
              <Route path="orders/tags" element={<TagManagePage />} />
              <Route path="transactions" element={<TransactionListPage />} />
              <Route path="transactions/categories" element={<TransactionCategoryManagePage />} />
              <Route path="reports" element={<ReportPage />} />
              <Route path="stock/ingredients" element={<IngredientListPage />} />
              <Route path="stock/records" element={<StockRecordPage />} />
              <Route path="stock/warnings" element={<StockWarningPage />} />
              <Route path="members" element={<MemberListPage />} />
              <Route path="members/points" element={<PointsRecordPage />} />
              <Route path="members/exchange" element={<PointsExchangePage />} />
              <Route path="backup" element={<BackupManagePage />} />
              <Route path="backup/settings" element={<BackupSettingsPage />} />
              <Route path="setting/staff" element={<StaffManagementPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AntApp>
    </ConfigProvider>
  );
};

export default App;
