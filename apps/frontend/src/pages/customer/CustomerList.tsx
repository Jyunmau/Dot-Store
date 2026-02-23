/**
 * Dot-Store V2.2 客户账户列表页面
 * 遵循设计规范：触摸目标≥44px，按钮高度≥48px
 */
import React, { useEffect, useState } from 'react';
import {
  Card,
  Button,
  Space,
  Tag,
  Modal,
  message,
  Input,
  Select,
  Pagination,
  List,
  Typography,
  Descriptions,
  Divider,
  Form,
  InputNumber,
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  ReloadOutlined,
  PhoneOutlined,
  UserOutlined,
  DollarOutlined,
  HistoryOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { customerService } from '@/services/customerService';
import type {
  CustomerAccount,
  CustomerAccountFilters,
  CustomerTransaction,
} from '@/types/customer';
import {
  getCustomerAccountStatusLabel,
  getCustomerTransactionTypeLabel,
  getCustomerTransactionTypeColor,
  CUSTOMER_ACCOUNT_STATUS_OPTIONS,
} from '@/types/customer';

const { Text } = Typography;

const MOBILE_BREAKPOINT = 768;
const TOUCH_TARGET_MIN = 44;

/**
 * 判断是否为移动端
 */
const useIsMobile = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);
    return () => window.removeEventListener('resize', checkIsMobile);
  }, []);

  return isMobile;
};

/**
 * 客户账户列表页面组件
 */
const CustomerListPage: React.FC = () => {
  const [accounts, setAccounts] = useState<CustomerAccount[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState<CustomerAccountFilters>({});
  
  const [createModal, setCreateModal] = useState(false);
  const [rechargeModal, setRechargeModal] = useState<{ visible: boolean; account: CustomerAccount | null }>({
    visible: false,
    account: null,
  });
  const [detailModal, setDetailModal] = useState<{ visible: boolean; account: CustomerAccount | null; transactions: CustomerTransaction[] }>({
    visible: false,
    account: null,
    transactions: [],
  });
  
  const [createForm] = Form.useForm();
  const [rechargeForm] = Form.useForm();
  
  const isMobile = useIsMobile();

  /**
   * 加载客户账户列表
   */
  const loadAccounts = async () => {
    setIsLoading(true);
    try {
      const response = await customerService.listAccounts({
        ...filters,
        page,
        page_size: pageSize,
      });
      setAccounts(response.items);
      setTotal(response.total);
    } catch (error) {
      message.error('加载客户账户失败');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, [filters, page, pageSize]);

  /**
   * 创建客户账户
   */
  const handleCreate = async (values: { customer_name: string; phone: string }) => {
    try {
      await customerService.createAccount(values);
      message.success('创建客户账户成功');
      setCreateModal(false);
      createForm.resetFields();
      loadAccounts();
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } };
      message.error(err.response?.data?.detail || '创建客户账户失败');
    }
  };

  /**
   * 客户充值
   */
  const handleRecharge = async (values: { amount: number; note?: string }) => {
    if (!rechargeModal.account) return;
    
    try {
      await customerService.recharge(rechargeModal.account.id, values);
      message.success('充值成功');
      setRechargeModal({ visible: false, account: null });
      rechargeForm.resetFields();
      loadAccounts();
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } };
      message.error(err.response?.data?.detail || '充值失败');
    }
  };

  /**
   * 查看账户详情
   */
  const handleViewDetail = async (account: CustomerAccount) => {
    try {
      const response = await customerService.getTransactions(account.id, { page: 1, page_size: 20 });
      setDetailModal({
        visible: true,
        account,
        transactions: response.items,
      });
    } catch (error) {
      message.error('加载交易记录失败');
    }
  };

  /**
   * 处理筛选条件变化
   */
  const handleFilterChange = (key: keyof CustomerAccountFilters, value: unknown) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
    setPage(1);
  };

  /**
   * 重置筛选条件
   */
  const handleReset = () => {
    setFilters({});
    setPage(1);
  };

  /**
   * 渲染账户卡片
   */
  const renderAccountCard = (account: CustomerAccount) => (
    <Card
      key={account.id}
      style={{ marginBottom: 12, borderRadius: 8 }}
      styles={{ body: { padding: 12 } }}
      onClick={() => handleViewDetail(account)}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <UserOutlined style={{ color: '#3B82F6' }} />
            <Text strong style={{ fontSize: 14 }}>{account.customer_name}</Text>
          </div>
          <div style={{ marginTop: 4, display: 'flex', alignItems: 'center', gap: 4 }}>
            <PhoneOutlined style={{ fontSize: 12, color: '#6B7280' }} />
            <Text type="secondary" style={{ fontSize: 12 }}>{account.phone}</Text>
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <Text strong style={{ fontSize: 18, color: '#52C41A' }}>
            ¥{parseFloat(account.balance).toFixed(2)}
          </Text>
          <div>
            <Tag color={account.status === 'active' ? 'green' : 'red'} style={{ marginTop: 4 }}>
              {getCustomerAccountStatusLabel(account.status)}
            </Tag>
          </div>
        </div>
      </div>
      
      <div style={{ display: 'flex', gap: 16, fontSize: 12, color: '#6B7280', marginBottom: 8 }}>
        <span>充值: ¥{parseFloat(account.total_recharged).toFixed(2)}</span>
        <span>消费: ¥{parseFloat(account.total_consumed).toFixed(2)}</span>
      </div>
      
      <div style={{ display: 'flex', gap: 8, marginTop: 8, paddingTop: 8, borderTop: '1px solid #F3F4F6' }}>
        <Button
          type="primary"
          size="small"
          icon={<DollarOutlined />}
          onClick={(e) => {
            e.stopPropagation();
            setRechargeModal({ visible: true, account });
          }}
          style={{ flex: 1, height: TOUCH_TARGET_MIN }}
        >
          充值
        </Button>
        <Button
          size="small"
          icon={<HistoryOutlined />}
          onClick={(e) => {
            e.stopPropagation();
            handleViewDetail(account);
          }}
          style={{ flex: 1, height: TOUCH_TARGET_MIN }}
        >
          明细
        </Button>
      </div>
    </Card>
  );

  return (
    <div style={{ padding: isMobile ? '12px' : '24px', background: isMobile ? '#F9FAFB' : 'transparent' }}>
      {/* 页面标题和操作按钮 */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: isMobile ? 0 : 16,
        padding: isMobile ? '12px 16px' : 0,
        background: isMobile ? '#fff' : 'transparent',
      }}>
        <Text strong style={{ fontSize: isMobile ? 16 : 20 }}>客户账户</Text>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setCreateModal(true)}
          style={{ height: isMobile ? TOUCH_TARGET_MIN : 32 }}
        >
          新增客户
        </Button>
      </div>

      {/* 筛选区域 */}
      <div style={{ padding: isMobile ? '12px 16px' : 0, background: isMobile ? '#fff' : 'transparent', marginBottom: isMobile ? 12 : 16 }}>
        <Space size="middle" wrap>
          <Input
            placeholder="搜索客户名称/手机号"
            prefix={<SearchOutlined />}
            style={{ width: isMobile ? '100%' : 200 }}
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            allowClear
          />
          <Select
            placeholder="账户状态"
            allowClear
            style={{ width: isMobile ? '100%' : 120 }}
            value={filters.status}
            onChange={(value) => handleFilterChange('status', value)}
            options={CUSTOMER_ACCOUNT_STATUS_OPTIONS}
          />
          <Button icon={<ReloadOutlined />} onClick={handleReset}>
            重置
          </Button>
        </Space>
      </div>

      {/* 账户列表 */}
      {isMobile ? (
        <List
          dataSource={accounts}
          loading={isLoading}
          renderItem={renderAccountCard}
          locale={{ emptyText: '暂无客户账户' }}
        />
      ) : (
        <Card>
          <List
            dataSource={accounts}
            loading={isLoading}
            renderItem={renderAccountCard}
            locale={{ emptyText: '暂无客户账户' }}
          />
        </Card>
      )}

      {/* 分页 */}
      <div style={{
        marginTop: 16,
        display: 'flex',
        justifyContent: 'center',
        padding: isMobile ? '12px 16px' : 0,
        background: isMobile ? '#fff' : 'transparent',
      }}>
        <Pagination
          current={page}
          pageSize={pageSize}
          total={total}
          showSizeChanger={!isMobile}
          showQuickJumper={!isMobile}
          showTotal={(total) => `共 ${total} 条`}
          onChange={(newPage, newPageSize) => {
            setPage(newPage);
            setPageSize(newPageSize);
          }}
          simple={isMobile}
          size={isMobile ? 'small' : 'default'}
        />
      </div>

      {/* 创建客户弹窗 */}
      <Modal
        title="新增客户"
        open={createModal}
        onCancel={() => {
          setCreateModal(false);
          createForm.resetFields();
        }}
        footer={null}
        width={isMobile ? '100%' : 400}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        <Form form={createForm} onFinish={handleCreate} layout="vertical">
          <Form.Item
            name="customer_name"
            label="客户名称"
            rules={[{ required: true, message: '请输入客户名称' }]}
          >
            <Input placeholder="请输入客户名称" />
          </Form.Item>
          <Form.Item
            name="phone"
            label="手机号"
            rules={[
              { required: true, message: '请输入手机号' },
              { pattern: /^1[3-9]\d{9}$/, message: '手机号格式错误' },
            ]}
          >
            <Input placeholder="请输入手机号" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block style={{ height: TOUCH_TARGET_MIN }}>
              创建
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* 充值弹窗 */}
      <Modal
        title={`充值 - ${rechargeModal.account?.customer_name || ''}`}
        open={rechargeModal.visible}
        onCancel={() => {
          setRechargeModal({ visible: false, account: null });
          rechargeForm.resetFields();
        }}
        footer={null}
        width={isMobile ? '100%' : 400}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        <div style={{ marginBottom: 16, padding: 12, background: '#F9FAFB', borderRadius: 8 }}>
          <Text type="secondary">当前余额：</Text>
          <Text strong style={{ fontSize: 18, color: '#52C41A' }}>
            ¥{rechargeModal.account ? parseFloat(rechargeModal.account.balance).toFixed(2) : '0.00'}
          </Text>
        </div>
        <Form form={rechargeForm} onFinish={handleRecharge} layout="vertical">
          <Form.Item
            name="amount"
            label="充值金额"
            rules={[{ required: true, message: '请输入充值金额' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              min={0.01}
              precision={2}
              placeholder="请输入充值金额"
              prefix="¥"
            />
          </Form.Item>
          <Form.Item name="note" label="备注">
            <Input.TextArea placeholder="请输入备注（可选）" rows={2} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block style={{ height: TOUCH_TARGET_MIN }}>
              确认充值
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* 详情弹窗 */}
      <Modal
        title="客户详情"
        open={detailModal.visible}
        onCancel={() => setDetailModal({ visible: false, account: null, transactions: [] })}
        footer={null}
        width={isMobile ? '100%' : 600}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        {detailModal.account && (
          <div>
            <Descriptions column={isMobile ? 1 : 2} bordered size="small">
              <Descriptions.Item label="客户名称">{detailModal.account.customer_name}</Descriptions.Item>
              <Descriptions.Item label="手机号">{detailModal.account.phone}</Descriptions.Item>
              <Descriptions.Item label="当前余额">
                <Text strong style={{ color: '#52C41A', fontSize: 16 }}>
                  ¥{parseFloat(detailModal.account.balance).toFixed(2)}
                </Text>
              </Descriptions.Item>
              <Descriptions.Item label="状态">
                <Tag color={detailModal.account.status === 'active' ? 'green' : 'red'}>
                  {getCustomerAccountStatusLabel(detailModal.account.status)}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="累计充值">
                ¥{parseFloat(detailModal.account.total_recharged).toFixed(2)}
              </Descriptions.Item>
              <Descriptions.Item label="累计消费">
                ¥{parseFloat(detailModal.account.total_consumed).toFixed(2)}
              </Descriptions.Item>
            </Descriptions>

            <Divider>交易记录</Divider>
            
            {detailModal.transactions.length > 0 ? (
              <List
                dataSource={detailModal.transactions}
                renderItem={(item) => (
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    padding: '8px 0',
                    borderBottom: '1px solid #F3F4F6'
                  }}>
                    <div>
                      <Tag color={getCustomerTransactionTypeColor(item.transaction_type)}>
                        {getCustomerTransactionTypeLabel(item.transaction_type)}
                      </Tag>
                      <Text type="secondary" style={{ marginLeft: 8, fontSize: 12 }}>
                        {dayjs(item.created_at).format('MM-DD HH:mm')}
                      </Text>
                    </div>
                    <Text style={{ color: item.transaction_type === 'recharge' ? '#52C41A' : '#FF4D4F' }}>
                      {item.transaction_type === 'recharge' ? '+' : '-'}¥{parseFloat(item.amount).toFixed(2)}
                    </Text>
                  </div>
                )}
              />
            ) : (
              <Text type="secondary">暂无交易记录</Text>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default CustomerListPage;
