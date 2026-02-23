/**
 * Dot-Store V2.2 现金账户页面
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
  Form,
  InputNumber,
  DatePicker,
  Statistic,
  Row,
  Col,
} from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { cashService } from '@/services/cashService';
import type {
  CashAccount,
  CashTransaction,
  CashTransactionFilters,
  CashSummary,
} from '@/types/cash';
import {
  getCashTransactionTypeLabel,
  getCashTransactionTypeColor,
  getCashCategoryLabel,
  CASH_TRANSACTION_TYPE_OPTIONS,
  INCOME_CATEGORY_OPTIONS,
  EXPENSE_CATEGORY_OPTIONS,
} from '@/types/cash';

const { Text } = Typography;
const { RangePicker } = DatePicker;

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
 * 现金账户页面组件
 */
const CashAccountPage: React.FC = () => {
  const [account, setAccount] = useState<CashAccount | null>(null);
  const [summary, setSummary] = useState<CashSummary | null>(null);
  const [transactions, setTransactions] = useState<CashTransaction[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState<CashTransactionFilters>({});
  
  const [incomeModal, setIncomeModal] = useState(false);
  const [expenseModal, setExpenseModal] = useState(false);
  
  const [incomeForm] = Form.useForm();
  const [expenseForm] = Form.useForm();
  
  const isMobile = useIsMobile();

  /**
   * 加载现金账户信息
   */
  const loadAccount = async () => {
    try {
      const response = await cashService.getAccount();
      setAccount(response);
    } catch (error) {
      message.error('加载现金账户失败');
    }
  };

  /**
   * 加载交易记录
   */
  const loadTransactions = async () => {
    setIsLoading(true);
    try {
      const response = await cashService.getTransactions({
        ...filters,
        page,
        page_size: pageSize,
      });
      setTransactions(response.items);
      setTotal(response.total);
    } catch (error) {
      message.error('加载交易记录失败');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * 加载收支汇总
   */
  const loadSummary = async () => {
    try {
      const response = await cashService.getSummary(filters.start_date, filters.end_date);
      setSummary(response);
    } catch (error) {
      console.error('加载收支汇总失败', error);
    }
  };

  useEffect(() => {
    loadAccount();
  }, []);

  useEffect(() => {
    loadTransactions();
    loadSummary();
  }, [filters, page, pageSize]);

  /**
   * 记录收入
   */
  const handleRecordIncome = async (values: { amount: number; category: string; note?: string }) => {
    try {
      await cashService.recordIncome(values);
      message.success('记录收入成功');
      setIncomeModal(false);
      incomeForm.resetFields();
      loadAccount();
      loadTransactions();
      loadSummary();
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } };
      message.error(err.response?.data?.detail || '记录收入失败');
    }
  };

  /**
   * 记录支出
   */
  const handleRecordExpense = async (values: { amount: number; category: string; note?: string }) => {
    try {
      await cashService.recordExpense(values);
      message.success('记录支出成功');
      setExpenseModal(false);
      expenseForm.resetFields();
      loadAccount();
      loadTransactions();
      loadSummary();
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } };
      message.error(err.response?.data?.detail || '记录支出失败');
    }
  };

  /**
   * 处理日期范围变化
   */
  const handleDateRangeChange = (dates: [dayjs.Dayjs | null, dayjs.Dayjs | null] | null) => {
    if (dates && dates[0] && dates[1]) {
      setFilters((prev) => ({
        ...prev,
        start_date: dates[0]!.startOf('day').toISOString(),
        end_date: dates[1]!.endOf('day').toISOString(),
        page: 1,
      }));
    } else {
      setFilters((prev) => {
        const { start_date, end_date, ...rest } = prev;
        return rest;
      });
    }
    setPage(1);
  };

  /**
   * 处理筛选条件变化
   */
  const handleFilterChange = (key: keyof CashTransactionFilters, value: unknown) => {
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
   * 渲染交易卡片
   */
  const renderTransactionCard = (transaction: CashTransaction) => (
    <div
      key={transaction.id}
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '12px 0',
        borderBottom: '1px solid #F3F4F6',
      }}
    >
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Tag color={getCashTransactionTypeColor(transaction.transaction_type)}>
            {getCashTransactionTypeLabel(transaction.transaction_type)}
          </Tag>
          <Text>{getCashCategoryLabel(transaction.category)}</Text>
        </div>
        <div style={{ marginTop: 4 }}>
          <Text type="secondary" style={{ fontSize: 12 }}>
            {dayjs(transaction.created_at).format('YYYY-MM-DD HH:mm')}
          </Text>
          {transaction.note && (
            <Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
              {transaction.note}
            </Text>
          )}
        </div>
      </div>
      <Text
        strong
        style={{
          fontSize: 16,
          color: transaction.transaction_type === 'income' ? '#52C41A' : '#FF4D4F',
        }}
      >
        {transaction.transaction_type === 'income' ? '+' : '-'}¥{parseFloat(transaction.amount).toFixed(2)}
      </Text>
    </div>
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
        <Text strong style={{ fontSize: isMobile ? 16 : 20 }}>现金账户</Text>
        <Space>
          <Button
            type="primary"
            icon={<ArrowUpOutlined />}
            onClick={() => setIncomeModal(true)}
            style={{ height: isMobile ? TOUCH_TARGET_MIN : 32 }}
          >
            记收入
          </Button>
          <Button
            danger
            icon={<ArrowDownOutlined />}
            onClick={() => setExpenseModal(true)}
            style={{ height: isMobile ? TOUCH_TARGET_MIN : 32 }}
          >
            记支出
          </Button>
        </Space>
      </div>

      {/* 账户信息卡片 */}
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={8}>
            <Statistic
              title="当前余额"
              value={account ? parseFloat(account.balance) : 0}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#3B82F6', fontSize: isMobile ? 24 : 32 }}
            />
          </Col>
          <Col xs={12} sm={8}>
            <Statistic
              title="累计收入"
              value={summary?.total_income || (account ? parseFloat(account.total_income) : 0)}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#52C41A' }}
            />
          </Col>
          <Col xs={12} sm={8}>
            <Statistic
              title="累计支出"
              value={summary?.total_expense || (account ? parseFloat(account.total_expense) : 0)}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#FF4D4F' }}
            />
          </Col>
        </Row>
      </Card>

      {/* 筛选区域 */}
      <div style={{ padding: isMobile ? '12px 16px' : 0, background: isMobile ? '#fff' : 'transparent', marginBottom: isMobile ? 12 : 16 }}>
        <Space size="middle" wrap>
          <RangePicker
            placeholder={['开始日期', '结束日期']}
            onChange={handleDateRangeChange}
            size={isMobile ? 'middle' : 'large'}
          />
          <Select
            placeholder="交易类型"
            allowClear
            style={{ width: isMobile ? '100%' : 120 }}
            value={filters.transaction_type}
            onChange={(value) => handleFilterChange('transaction_type', value)}
            options={CASH_TRANSACTION_TYPE_OPTIONS}
          />
          <Select
            placeholder="收支分类"
            allowClear
            style={{ width: isMobile ? '100%' : 150 }}
            value={filters.category}
            onChange={(value) => handleFilterChange('category', value)}
            options={[...INCOME_CATEGORY_OPTIONS, ...EXPENSE_CATEGORY_OPTIONS]}
          />
          <Button icon={<ReloadOutlined />} onClick={handleReset}>
            重置
          </Button>
        </Space>
      </div>

      {/* 交易列表 */}
      <Card>
        <List
          dataSource={transactions}
          loading={isLoading}
          renderItem={renderTransactionCard}
          locale={{ emptyText: '暂无交易记录' }}
        />
      </Card>

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

      {/* 记录收入弹窗 */}
      <Modal
        title="记录收入"
        open={incomeModal}
        onCancel={() => {
          setIncomeModal(false);
          incomeForm.resetFields();
        }}
        footer={null}
        width={isMobile ? '100%' : 400}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        <Form form={incomeForm} onFinish={handleRecordIncome} layout="vertical">
          <Form.Item
            name="amount"
            label="收入金额"
            rules={[{ required: true, message: '请输入收入金额' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              min={0.01}
              precision={2}
              placeholder="请输入收入金额"
              prefix="¥"
            />
          </Form.Item>
          <Form.Item
            name="category"
            label="收入分类"
            rules={[{ required: true, message: '请选择收入分类' }]}
          >
            <Select placeholder="请选择收入分类" options={INCOME_CATEGORY_OPTIONS} />
          </Form.Item>
          <Form.Item name="note" label="备注">
            <Input.TextArea placeholder="请输入备注（可选）" rows={2} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block style={{ height: TOUCH_TARGET_MIN }}>
              确认记录
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* 记录支出弹窗 */}
      <Modal
        title="记录支出"
        open={expenseModal}
        onCancel={() => {
          setExpenseModal(false);
          expenseForm.resetFields();
        }}
        footer={null}
        width={isMobile ? '100%' : 400}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        <div style={{ marginBottom: 16, padding: 12, background: '#FFF7E6', borderRadius: 8 }}>
          <Text type="secondary">当前余额：</Text>
          <Text strong style={{ fontSize: 18, color: '#3B82F6' }}>
            ¥{account ? parseFloat(account.balance).toFixed(2) : '0.00'}
          </Text>
        </div>
        <Form form={expenseForm} onFinish={handleRecordExpense} layout="vertical">
          <Form.Item
            name="amount"
            label="支出金额"
            rules={[{ required: true, message: '请输入支出金额' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              min={0.01}
              precision={2}
              placeholder="请输入支出金额"
              prefix="¥"
            />
          </Form.Item>
          <Form.Item
            name="category"
            label="支出分类"
            rules={[{ required: true, message: '请选择支出分类' }]}
          >
            <Select placeholder="请选择支出分类" options={EXPENSE_CATEGORY_OPTIONS} />
          </Form.Item>
          <Form.Item name="note" label="备注">
            <Input.TextArea placeholder="请输入备注（可选）" rows={2} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" danger htmlType="submit" block style={{ height: TOUCH_TARGET_MIN }}>
              确认支出
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CashAccountPage;
