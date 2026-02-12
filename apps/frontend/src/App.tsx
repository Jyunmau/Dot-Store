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
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Dot-Store</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">欢迎，{user?.shop_name}</span>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
            >
              退出登录
            </button>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 px-4">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">欢迎使用 Dot-Store 点单收银系统</h2>
          <p className="text-gray-600">当前版本：V2.1</p>
          <p className="text-gray-600 mt-2">店铺类型：{user?.shop_type}</p>
          <p className="text-gray-600 mt-2">所在城市：{user?.city}</p>
        </div>
      </main>
    </div>
  );
};

/**
 * 主布局组件
 */
const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">Dot-Store</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">欢迎，{user?.shop_name}</span>
          </div>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
};

const App: React.FC = () => {
  const { isAuthenticated, token } = useAuthStore();

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
                  <HomePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/setting/staff"
              element={
                <ProtectedRoute>
                  <MainLayout>
                    <StaffManagementPage />
                  </MainLayout>
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AntApp>
    </ConfigProvider>
  );
};

export default App;
