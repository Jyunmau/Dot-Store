/**
 * Dot-Store V2.2 成本记录页面
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
  Popconfirm,
} from 'antd';
import {
  PlusOutlined,
  ReloadOutlined,
  DeleteOutlined,
  EditOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { expenseService } from '@/services/expenseService';
import type {
  ExpenseRecord,
  ExpenseFilters,
  ExpenseSummary,
  CreateExpenseParams,
  UpdateExpenseParams,
} from '@/types/expense';
import {
  EXPENSE_CATEGORY_OPTIONS,
  COST_BEHAVIOR_OPTIONS,
  COST_FUNCTION_OPTIONS,
  getExpenseCategoryLabel,
  getExpenseCategoryColor,
  getCostBehaviorLabel,
} from '@/types/expense';

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
 * 成本记录页面组件
 */
const ExpenseRecordPage: React.FC = () => {
  const [expenses, setExpenses] = useState<ExpenseRecord[]>([]);
  const [summary, setSummary] = useState<ExpenseSummary | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState<ExpenseFilters>({});
  
  const [formModal, setFormModal] = useState(false);
  const [editingExpense, setEditingExpense] = useState<ExpenseRecord | null>(null);
  
  const [form] = Form.useForm();
  
  const isMobile = useIsMobile();

  /**
   * 加载成本记录列表
   */
  const loadExpenses = async () => {
    setIsLoading(true);
    try {
      const response = await expenseService.getExpenses({
        ...filters,
        page,
        page_size: pageSize,
      });
      setExpenses(response.items);
      setTotal(response.total);
    } catch (error) {
      message.error('加载成本记录失败');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * 加载成本汇总
   */
  const loadSummary = async () => {
    try {
      const response = await expenseService.getSummary(filters.start_date, filters.end_date);
      setSummary(response);
    } catch (error) {
      console.error('加载成本汇总失败', error);
    }
  };

  useEffect(() => {
    loadExpenses();
    loadSummary();
  }, [filters, page, pageSize]);

  /**
   * 打开创建弹窗
   */
  const handleCreate = () => {
    setEditingExpense(null);
    form.resetFields();
    form.setFieldsValue({
      expense_date: dayjs().format('YYYY-MM-DD'),
    });
    setFormModal(true);
  };

  /**
   * 打开编辑弹窗
   */
  const handleEdit = (expense: ExpenseRecord) => {
    setEditingExpense(expense);
    form.setFieldsValue({
      category: expense.category,
      amount: parseFloat(expense.amount),
      description: expense.description,
      expense_date: expense.expense_date,
      cost_behavior: expense.cost_behavior,
      cost_function: expense.cost_function,
    });
    setFormModal(true);
  };

  /**
   * 提交表单
   */
  const handleSubmit = async (values: CreateExpenseParams | UpdateExpenseParams) => {
    try {
      if (editingExpense) {
        await expenseService.updateExpense(editingExpense.id, values);
        message.success('更新成本记录成功');
      } else {
        await expenseService.createExpense(values as CreateExpenseParams);
        message.success('创建成本记录成功');
      }
      setFormModal(false);
      form.resetFields();
      loadExpenses();
      loadSummary();
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } };
      message.error(err.response?.data?.detail || '操作失败');
    }
  };

  /**
   * 删除成本记录
   */
  const handleDelete = async (id: number) => {
    try {
      await expenseService.deleteExpense(id);
      message.success('删除成功');
      loadExpenses();
      loadSummary();
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } };
      message.error(err.response?.data?.detail || '删除失败');
    }
  };

  /**
   * 处理日期范围变化
   */
  const handleDateRangeChange = (dates: [dayjs.Dayjs | null, dayjs.Dayjs | null] | null) => {
    if (dates && dates[0] && dates[1]) {
      setFilters((prev) => ({
        ...prev,
        start_date: dates[0]!.format('YYYY-MM-DD'),
        end_date: dates[1]!.format('YYYY-MM-DD'),
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
  const handleFilterChange = (key: keyof ExpenseFilters, value: unknown) => {
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
   * 渲染成本记录卡片
   */
  const renderExpenseCard = (expense: ExpenseRecord) => (
    <div
      key={expense.id}
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '12px 0',
        borderBottom: '1px solid #F3F4F6',
      }}
    >
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Tag color={getExpenseCategoryColor(expense.category)}>
            {getExpenseCategoryLabel(expense.category)}
          </Tag>
          {expense.cost_behavior && (
            <Tag color="blue">{getCostBehaviorLabel(expense.cost_behavior)}</Tag>
          )}
        </div>
        <div style={{ marginTop: 4 }}>
          <Text type="secondary" style={{ fontSize: 12 }}>
            {dayjs(expense.expense_date).format('YYYY-MM-DD')}
          </Text>
          {expense.description && (
            <Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
              {expense.description}
            </Text>
          )}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <Text
          strong
          style={{
            fontSize: 16,
            color: '#FF4D4F',
          }}
        >
          -¥{parseFloat(expense.amount).toFixed(2)}
        </Text>
        <Space size="small">
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => handleEdit(expense)}
            style={{ minWidth: TOUCH_TARGET_MIN, height: TOUCH_TARGET_MIN }}
          />
          <Popconfirm
            title="确定要删除这条成本记录吗？"
            onConfirm={() => handleDelete(expense.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
              style={{ minWidth: TOUCH_TARGET_MIN, height: TOUCH_TARGET_MIN }}
            />
          </Popconfirm>
        </Space>
      </div>
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
        <Text strong style={{ fontSize: isMobile ? 16 : 20 }}>成本记录</Text>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleCreate}
          style={{ height: isMobile ? TOUCH_TARGET_MIN : 32 }}
        >
          新增成本
        </Button>
      </div>

      {/* 成本汇总卡片 */}
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={8}>
            <Statistic
              title="总成本"
              value={summary?.total_amount || 0}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#FF4D4F', fontSize: isMobile ? 24 : 32 }}
            />
          </Col>
          <Col xs={12} sm={8}>
            <Statistic
              title="记录数量"
              value={total}
              suffix="条"
            />
          </Col>
          <Col xs={12} sm={8}>
            <Statistic
              title="平均成本"
              value={total > 0 ? (summary?.total_amount || 0) / total : 0}
              precision={2}
              prefix="¥"
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
            placeholder="成本分类"
            allowClear
            style={{ width: isMobile ? '100%' : 120 }}
            value={filters.category}
            onChange={(value) => handleFilterChange('category', value)}
            options={EXPENSE_CATEGORY_OPTIONS}
          />
          <Select
            placeholder="成本行为"
            allowClear
            style={{ width: isMobile ? '100%' : 120 }}
            value={filters.cost_behavior}
            onChange={(value) => handleFilterChange('cost_behavior', value)}
            options={COST_BEHAVIOR_OPTIONS}
          />
          <Button icon={<ReloadOutlined />} onClick={handleReset}>
            重置
          </Button>
        </Space>
      </div>

      {/* 成本记录列表 */}
      <Card>
        <List
          dataSource={expenses}
          loading={isLoading}
          renderItem={renderExpenseCard}
          locale={{ emptyText: '暂无成本记录' }}
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

      {/* 创建/编辑弹窗 */}
      <Modal
        title={editingExpense ? '编辑成本记录' : '新增成本记录'}
        open={formModal}
        onCancel={() => {
          setFormModal(false);
          form.resetFields();
        }}
        footer={null}
        width={isMobile ? '100%' : 400}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        <Form form={form} onFinish={handleSubmit} layout="vertical">
          <Form.Item
            name="category"
            label="成本分类"
            rules={[{ required: true, message: '请选择成本分类' }]}
          >
            <Select placeholder="请选择成本分类" options={EXPENSE_CATEGORY_OPTIONS} />
          </Form.Item>
          <Form.Item
            name="amount"
            label="成本金额"
            rules={[{ required: true, message: '请输入成本金额' }]}
          >
            <InputNumber
              style={{ width: '100%' }}
              min={0.01}
              precision={2}
              placeholder="请输入成本金额"
              prefix="¥"
            />
          </Form.Item>
          <Form.Item
            name="expense_date"
            label="成本日期"
            rules={[{ required: true, message: '请选择成本日期' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="cost_behavior" label="成本行为">
            <Select placeholder="请选择成本行为（可选）" allowClear options={COST_BEHAVIOR_OPTIONS} />
          </Form.Item>
          <Form.Item name="cost_function" label="成本功能">
            <Select placeholder="请选择成本功能（可选）" allowClear options={COST_FUNCTION_OPTIONS} />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea placeholder="请输入描述（可选）" rows={2} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block style={{ height: TOUCH_TARGET_MIN }}>
              {editingExpense ? '保存修改' : '确认创建'}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ExpenseRecordPage;
