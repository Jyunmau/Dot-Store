/**
 * 注册页面
 */
import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Select, Steps, Space } from 'antd';
import { LockOutlined, MobileOutlined, MailOutlined, ShopOutlined, EnvironmentOutlined } from '@ant-design/icons';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';

const { Option } = Select;

const SHOP_TYPES = [
  { value: 'restaurant', label: '餐饮店' },
  { value: 'cafe', label: '咖啡店' },
  { value: 'bakery', label: '烘焙店' },
  { value: 'tea', label: '茶饮店' },
  { value: 'snack', label: '小吃店' },
  { value: 'other', label: '其他' },
];

interface StepOneValues {
  phone?: string;
  email?: string;
  password: string;
  confirmPassword: string;
}

interface StepTwoValues {
  shop_name: string;
  shop_type: string;
  city: string;
}

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register, loading, error } = useAuthStore();
  const [currentStep, setCurrentStep] = useState(0);
  const [registerType, setRegisterType] = useState<'phone' | 'email'>('phone');
  const [stepOneValues, setStepOneValues] = useState<StepOneValues | null>(null);
  const [form] = Form.useForm();

  const handleSubmit = async (values: StepTwoValues) => {
    if (!stepOneValues) {
      message.error('请先完成账户信息');
      setCurrentStep(0);
      return;
    }

    if (stepOneValues.password !== stepOneValues.confirmPassword) {
      message.error('两次输入的密码不一致');
      return;
    }

    try {
      await register({
        phone: registerType === 'phone' ? stepOneValues.phone : undefined,
        email: registerType === 'email' ? stepOneValues.email : undefined,
        password: stepOneValues.password,
        shop_name: values.shop_name,
        shop_type: values.shop_type,
        city: values.city,
      });
      message.success('注册成功');
      navigate('/');
    } catch {
      message.error(error || '注册失败');
    }
  };

  const handleNextStep = () => {
    form.validateFields(['phone', 'email', 'password', 'confirmPassword'])
      .then((values) => {
        setStepOneValues(values);
        setCurrentStep(1);
      })
      .catch(() => {
        message.error('请完善账户信息');
      });
  };

  const handleRegisterTypeChange = (type: 'phone' | 'email') => {
    setRegisterType(type);
    form.setFieldsValue({ phone: undefined, email: undefined });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-lg shadow-xl">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Dot-Store</h1>
          <p className="mt-2 text-gray-600">创建您的店铺账号</p>
        </div>

        <Steps
          current={currentStep}
          size="small"
          className="mb-6"
          items={[
            { title: '账户信息' },
            { title: '店铺信息' },
          ]}
        />

        <Form
          form={form}
          onFinish={handleSubmit}
          layout="vertical"
          size="large"
          preserve={true}
        >
          {currentStep === 0 && (
            <>
              <div className="flex justify-center mb-4">
                <Space.Compact>
                  <Button
                    type={registerType === 'phone' ? 'primary' : 'default'}
                    onClick={() => handleRegisterTypeChange('phone')}
                  >
                    手机号注册
                  </Button>
                  <Button
                    type={registerType === 'email' ? 'primary' : 'default'}
                    onClick={() => handleRegisterTypeChange('email')}
                  >
                    邮箱注册
                  </Button>
                </Space.Compact>
              </div>

              {registerType === 'phone' ? (
                <Form.Item
                  name="phone"
                  label="手机号"
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
              ) : (
                <Form.Item
                  name="email"
                  label="邮箱"
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
              )}

              <Form.Item
                name="password"
                label="密码"
                rules={[
                  { required: true, message: '请输入密码' },
                  { min: 8, message: '密码至少8位' },
                  { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/, message: '密码需包含字母和数字' },
                ]}
              >
                <Input.Password
                  prefix={<LockOutlined className="text-gray-400" />}
                  placeholder="请输入密码（至少8位，包含字母和数字）"
                />
              </Form.Item>

              <Form.Item
                name="confirmPassword"
                label="确认密码"
                dependencies={['password']}
                rules={[
                  { required: true, message: '请确认密码' },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('两次输入的密码不一致'));
                    },
                  }),
                ]}
              >
                <Input.Password
                  prefix={<LockOutlined className="text-gray-400" />}
                  placeholder="请再次输入密码"
                />
              </Form.Item>

              <Button
                type="primary"
                block
                onClick={handleNextStep}
                className="h-12"
              >
                下一步
              </Button>
            </>
          )}

          {currentStep === 1 && (
            <>
              <Form.Item
                name="shop_name"
                label="店铺名称"
                rules={[{ required: true, message: '请输入店铺名称' }]}
              >
                <Input
                  prefix={<ShopOutlined className="text-gray-400" />}
                  placeholder="请输入店铺名称"
                />
              </Form.Item>

              <Form.Item
                name="shop_type"
                label="店铺类型"
                rules={[{ required: true, message: '请选择店铺类型' }]}
              >
                <Select placeholder="请选择店铺类型">
                  {SHOP_TYPES.map((type) => (
                    <Option key={type.value} value={type.value}>
                      {type.label}
                    </Option>
                  ))}
                </Select>
              </Form.Item>

              <Form.Item
                name="city"
                label="所在城市"
                rules={[{ required: true, message: '请输入所在城市' }]}
              >
                <Input
                  prefix={<EnvironmentOutlined className="text-gray-400" />}
                  placeholder="请输入所在城市"
                />
              </Form.Item>

              <div className="flex gap-4">
                <Button
                  block
                  onClick={() => setCurrentStep(0)}
                  className="h-12"
                >
                  上一步
                </Button>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  block
                  className="h-12"
                >
                  注册
                </Button>
              </div>
            </>
          )}
        </Form>

        <div className="text-center mt-4">
          <span className="text-gray-600">已有账号？</span>
          <Link to="/login" className="text-blue-600 hover:text-blue-700 ml-1">
            立即登录
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default RegisterPage;
