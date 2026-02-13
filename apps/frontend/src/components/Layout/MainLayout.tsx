/**
 * 主布局组件
 * 支持响应式布局：移动端底部导航，桌面端侧边导航
 */
import React, { useState, useEffect } from 'react';
import { Layout, Menu, Avatar, Dropdown, Button, Space, Drawer } from 'antd';
import {
  OrderedListOutlined,
  DeleteOutlined,
  TagsOutlined,
  AppstoreOutlined,
  LogoutOutlined,
  UserOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DollarOutlined,
  WalletOutlined,
  BarChartOutlined,
  TeamOutlined,
  TrophyOutlined,
  SwapOutlined,
  InboxOutlined,
  DatabaseOutlined,
  WarningOutlined,
  CloudServerOutlined,
  SettingOutlined,
  HomeOutlined,
  MenuOutlined,
  BellOutlined,
  UsergroupAddOutlined,
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
   * 底部导航项
   */
  const bottomNavItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
    },
    {
      key: '/orders',
      icon: <OrderedListOutlined />,
      label: '订单',
    },
    {
      key: '/transactions',
      icon: <DollarOutlined />,
      label: '收支',
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
   * 侧边菜单项
   */
  const menuItems = [
    {
      key: '/orders',
      icon: <OrderedListOutlined />,
      label: '订单列表',
    },
    {
      key: '/orders/recycle',
      icon: <DeleteOutlined />,
      label: '回收站',
    },
    {
      key: '/orders/categories',
      icon: <AppstoreOutlined />,
      label: '订单分类',
    },
    {
      key: '/orders/tags',
      icon: <TagsOutlined />,
      label: '订单标签',
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/transactions',
      icon: <DollarOutlined />,
      label: '收支记录',
    },
    {
      key: '/transactions/categories',
      icon: <WalletOutlined />,
      label: '收支分类',
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/reports',
      icon: <BarChartOutlined />,
      label: '经营报表',
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/stock/ingredients',
      icon: <InboxOutlined />,
      label: '食材管理',
    },
    {
      key: '/stock/records',
      icon: <DatabaseOutlined />,
      label: '库存记录',
    },
    {
      key: '/stock/warnings',
      icon: <WarningOutlined />,
      label: '库存预警',
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
      key: '/members/points',
      icon: <TrophyOutlined />,
      label: '积分记录',
    },
    {
      key: '/members/exchange',
      icon: <SwapOutlined />,
      label: '积分兑换',
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/backup',
      icon: <CloudServerOutlined />,
      label: '备份管理',
    },
    {
      key: '/backup/settings',
      icon: <SettingOutlined />,
      label: '备份设置',
    },
    {
      type: 'divider' as const,
    },
    {
      key: '/setting/staff',
      icon: <UsergroupAddOutlined />,
      label: '店员管理',
    },
    {
      key: '/setting/notification',
      icon: <BellOutlined />,
      label: '通知设置',
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
            Dot Store
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
            selectedKeys={[location.pathname]}
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
            {collapsed ? 'Dot' : 'Dot Store'}
          </h1>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
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
