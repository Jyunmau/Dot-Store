/**
 * 登录页面
 */
import React, { useState } from 'react';
import { Form, Input, Button, Card, Tabs, App } from 'antd';
import { MobileOutlined, MailOutlined, LockOutlined } from '@ant-design/icons';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { AxiosError } from 'axios';

interface LoginForm {
  username: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, loading, clearError } = useAuthStore();
  const [loginType, setLoginType] = useState<'phone' | 'email'>('phone');
  const [form] = Form.useForm();
  const { message } = App.useApp();

  const handleSubmit = async (values: LoginForm) => {
    try {
      await login(values.username, values.password);
      message.success('登录成功');
      navigate('/');
    } catch (error: unknown) {
      let errorMessage = '登录失败';
      
      if (error instanceof AxiosError) {
        if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
          errorMessage = '请求失败，请检查网络';
        } else if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
          errorMessage = '请求失败，请检查网络';
        } else if (error.response?.status === 401) {
          errorMessage = '账号或密码不正确';
        } else if (error.response?.status === 422) {
          errorMessage = '账号或密码不正确';
        } else if (error.response?.data?.detail) {
          const detail = error.response.data.detail;
          if (typeof detail === 'string') {
            errorMessage = detail;
          } else if (Array.isArray(detail) && detail.length > 0) {
            errorMessage = detail[0].msg || '账号或密码不正确';
          }
        }
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      message.error({
        content: errorMessage,
        duration: 3,
      });
    }
  };

  const handleTabChange = (key: string) => {
    setLoginType(key as 'phone' | 'email');
    form.resetFields();
    clearError();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md shadow-xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dot-Store</h1>
          <p className="mt-2 text-gray-600">点单收银系统</p>
        </div>

        <Tabs
          activeKey={loginType}
          onChange={handleTabChange}
          centered
          items={[
            {
              key: 'phone',
              label: '手机号登录',
              children: (
                <Form
                  form={form}
                  onFinish={handleSubmit}
                  layout="vertical"
                  size="large"
                >
                  <Form.Item
                    name="username"
                    rules={[
                      { required: true, message: '请输入手机号' },
                      { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' },
                    ]}
                  >
                    <Input
                      prefix={<MobileOutlined className="text-gray-400" />}
                      placeholder="请输入手机号"
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[
                      { required: true, message: '请输入密码' },
                      { min: 8, message: '密码至少8位' },
                    ]}
                  >
                    <Input.Password
                      prefix={<LockOutlined className="text-gray-400" />}
                      placeholder="请输入密码"
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button
                      type="primary"
                      htmlType="submit"
                      loading={loading}
                      block
                      className="h-12"
                    >
                      登录
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
            {
              key: 'email',
              label: '邮箱登录',
              children: (
                <Form
                  form={form}
                  onFinish={handleSubmit}
                  layout="vertical"
                  size="large"
                >
                  <Form.Item
                    name="username"
                    rules={[
                      { required: true, message: '请输入邮箱' },
                      { type: 'email', message: '邮箱格式不正确' },
                    ]}
                  >
                    <Input
                      prefix={<MailOutlined className="text-gray-400" />}
                      placeholder="请输入邮箱"
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[
                      { required: true, message: '请输入密码' },
                      { min: 8, message: '密码至少8位' },
                    ]}
                  >
                    <Input.Password
                      prefix={<LockOutlined className="text-gray-400" />}
                      placeholder="请输入密码"
                    />
                  </Form.Item>

                  <Form.Item>
                    <Button
                      type="primary"
                      htmlType="submit"
                      loading={loading}
                      block
                      className="h-12"
                    >
                      登录
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
          ]}
        />

        <div className="text-center mt-4">
          <span className="text-gray-600">还没有账号？</span>
          <Link to="/register" className="text-blue-600 hover:text-blue-700 ml-1">
            立即注册
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default LoginPage;
