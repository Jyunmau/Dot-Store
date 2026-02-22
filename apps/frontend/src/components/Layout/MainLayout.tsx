/**
 * Dot-Store V2.2 主布局组件
 * 支持响应式布局：移动端底部导航，桌面端侧边导航
 */
import React, { useState, useEffect } from 'react';
import { Layout, Menu, Avatar, Dropdown, Button, Space, Drawer } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  BulbOutlined,
  BarChartOutlined,
  SettingOutlined,
  LogoutOutlined,
  UserOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  OrderedListOutlined,
  DollarOutlined,
  InboxOutlined,
  HistoryOutlined,
  WarningOutlined,
  BellOutlined,
  UsergroupAddOutlined,
  MenuOutlined,
  SafetyCertificateOutlined,
  TeamOutlined,
  CloudServerOutlined,
} from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { NetworkStatus } from '@/components/PWA';

const { Sider, Content, Header } = Layout;

/**
 * 判断是否为移动端
 */
const useIsMobile = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);
    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  return isMobile;
};

/**
 * 主布局组件
 */
const MainLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [drawerVisible, setDrawerVisible] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuthStore();
  const isMobile = useIsMobile();

  /**
   * 处理菜单点击
   */
  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
    if (isMobile) {
      setDrawerVisible(false);
    }
  };

  /**
   * 处理退出登录
   */
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  /**
   * V2.2 底部导航项
   */
  const bottomNavItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      key: '/records/orders',
      icon: <FileTextOutlined />,
      label: '记录',
    },
    {
      key: '/insights/income',
      icon: <BulbOutlined />,
      label: '洞察',
    },
    {
      key: '/reports',
      icon: <BarChartOutlined />,
      label: '报表',
    },
    {
      key: 'menu',
      icon: <MenuOutlined />,
      label: '更多',
    },
  ];

  /**
   * V2.2 侧边菜单项
   */
  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'records',
      icon: <FileTextOutlined />,
      label: '记录',
      children: [
        {
          key: '/records/orders',
          icon: <OrderedListOutlined />,
          label: '订单',
        },
        {
          key: '/records/transactions',
          icon: <DollarOutlined />,
          label: '收支',
        },
        {
          key: '/records/stock',
          icon: <InboxOutlined />,
          label: '库存',
        },
      ],
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'insights',
      icon: <BulbOutlined />,
      label: '洞察',
      children: [
        {
          key: '/insights/income',
          icon: <DollarOutlined />,
          label: '钱从哪里来',
        },
        {
          key: '/insights/cost',
          icon: <BarChartOutlined />,
          label: '钱花哪里了',
        },
        {
          key: '/insights/profit',
          icon: <SafetyCertificateOutlined />,
          label: '什么时候赚钱',
        },
        {
          key: '/insights/cashflow',
          icon: <HistoryOutlined />,
          label: '未来剩多少',
        },
      ],
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'reports',
      icon: <BarChartOutlined />,
      label: '报表',
      children: [
        {
          key: '/reports/daily',
          icon: <FileTextOutlined />,
          label: '日报',
        },
        {
          key: '/reports/weekly',
          icon: <FileTextOutlined />,
          label: '周报',
        },
        {
          key: '/reports/monthly',
          icon: <FileTextOutlined />,
          label: '月报',
        },
      ],
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/stock/warnings',
      icon: <WarningOutlined />,
      label: '库存预警',
    },
    {
      key: '/stock/transactions',
      icon: <HistoryOutlined />,
      label: '库存流水',
    },
    {
      key: '/events',
      icon: <HistoryOutlined />,
      label: '事件日志',
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '设置',
      children: [
        {
          key: '/settings/profile',
          icon: <UserOutlined />,
          label: '用户信息',
        },
        {
          key: '/settings/shop',
          icon: <DashboardOutlined />,
          label: '店铺信息',
        },
        {
          key: '/settings/notification',
          icon: <BellOutlined />,
          label: '提醒设置',
        },
        {
          key: '/settings/staff',
          icon: <UsergroupAddOutlined />,
          label: '店员管理',
        },
      ],
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/members',
      icon: <TeamOutlined />,
      label: '会员管理',
    },
    {
      key: '/backup',
      icon: <CloudServerOutlined />,
      label: '备份管理',
    },
  ];

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人信息',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      danger: true,
    },
  ];

  /**
   * 处理底部导航点击
   */
  const handleBottomNavClick = (key: string) => {
    if (key === 'menu') {
      setDrawerVisible(true);
    } else {
      navigate(key);
    }
  };

  /**
   * 获取当前选中的菜单键
   */
  const getSelectedKeys = () => {
    const path = location.pathname;
    return [path];
  };

  /**
   * 获取默认展开的菜单键
   */
  const getDefaultOpenKeys = () => {
    const path = location.pathname;
    if (path.startsWith('/records')) return ['records'];
    if (path.startsWith('/insights')) return ['insights'];
    if (path.startsWith('/reports')) return ['reports'];
    if (path.startsWith('/settings')) return ['settings'];
    return [];
  };

  /**
   * 移动端布局
   */
  if (isMobile) {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Header
          style={{
            padding: '0 16px',
            background: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            position: 'sticky',
            top: 0,
            zIndex: 100,
          }}
        >
          <h1 style={{ margin: 0, fontSize: 18, fontWeight: 'bold', color: '#1890ff' }}>
            Dot Store V2.2
          </h1>
          <div className="flex items-center gap-3">
            <NetworkStatus />
            <Dropdown
              menu={{
                items: userMenuItems,
                onClick: ({ key }) => {
                  if (key === 'logout') {
                    handleLogout();
                  }
                },
              }}
              placement="bottomRight"
            >
              <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
            </Dropdown>
          </div>
        </Header>
        
        <Content
          style={{
            margin: 0,
            background: '#f5f5f5',
            minHeight: 'calc(100vh - 64px - 64px)',
            paddingBottom: '64px',
            overflow: 'auto',
          }}
        >
          <Outlet />
        </Content>

        <div
          style={{
            position: 'fixed',
            bottom: 0,
            left: 0,
            right: 0,
            background: '#fff',
            borderTop: '1px solid #f0f0f0',
            display: 'flex',
            justifyContent: 'space-around',
            padding: '8px 0',
            zIndex: 100,
          }}
        >
          {bottomNavItems.map((item) => (
            <div
              key={item.key}
              onClick={() => handleBottomNavClick(item.key)}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                cursor: 'pointer',
                color: location.pathname === item.key ? '#1890ff' : '#666',
                padding: '4px 12px',
                minWidth: '48px',
                minHeight: '44px',
              }}
            >
              <span style={{ fontSize: '20px' }}>{item.icon}</span>
              <span style={{ fontSize: '12px', marginTop: '2px' }}>{item.label}</span>
            </div>
          ))}
        </div>

        <Drawer
          title="菜单"
          placement="right"
          onClose={() => setDrawerVisible(false)}
          open={drawerVisible}
          width={280}
        >
          <Menu
            mode="inline"
            selectedKeys={getSelectedKeys()}
            defaultOpenKeys={getDefaultOpenKeys()}
            items={menuItems}
            onClick={handleMenuClick}
            style={{ borderRight: 0 }}
          />
        </Drawer>
      </Layout>
    );
  }

  /**
   * 桌面端布局
   */
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        theme="light"
        width={240}
        style={{
          boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
        }}
      >
        <div
          style={{
            height: 64,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderBottom: '1px solid #f0f0f0',
          }}
        >
          <h1
            style={{
              margin: 0,
              fontSize: collapsed ? 16 : 20,
              fontWeight: 'bold',
              color: '#1890ff',
              whiteSpace: 'nowrap',
            }}
          >
            {collapsed ? 'Dot' : 'Dot Store V2.2'}
          </h1>
        </div>
        <Menu
          mode="inline"
          selectedKeys={getSelectedKeys()}
          defaultOpenKeys={getDefaultOpenKeys()}
          items={menuItems}
          onClick={handleMenuClick}
          style={{ borderRight: 0 }}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            padding: '0 24px',
            background: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ fontSize: 16 }}
          />
          <div className="flex items-center gap-4">
            <NetworkStatus />
            <Dropdown
              menu={{
                items: userMenuItems,
                onClick: ({ key }) => {
                  if (key === 'logout') {
                    handleLogout();
                  }
                },
              }}
              placement="bottomRight"
            >
              <Space style={{ cursor: 'pointer' }}>
                <Avatar icon={<UserOutlined />} />
                <span>{user?.shop_name || '用户'}</span>
              </Space>
            </Dropdown>
          </div>
        </Header>
        <Content
          style={{
            margin: 0,
            background: '#f5f5f5',
            minHeight: 'calc(100vh - 64px)',
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
