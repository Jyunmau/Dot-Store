/**
 * 收支记录列表页面
 */
import React, { useEffect, useState } from 'react';
import {
  Table,
  Button,
  Space,
  Tag,
  Modal,
  message,
  Popconfirm,
  Card,
  Select,
  DatePicker,
  Pagination,
  Statistic,
  Row,
  Col,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ReloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useTransactionStore } from '@/store/transactionStore';
import type { Transaction, TransactionFilters } from '@/types/transaction';
import {
  getTransactionTypeLabel,
  getTransactionTypeColor,
  TRANSACTION_TYPE_OPTIONS,
} from '@/types/transaction';
import TransactionForm from './TransactionForm';

const { RangePicker } = DatePicker;

/**
 * 收支记录列表页面组件
 */
const TransactionListPage: React.FC = () => {
  const {
    transactions,
    total,
    page,
    pageSize,
    isLoading,
    summary,
    listTransactions,
    deleteTransaction,
    getTransactionSummary,
    listCategories,
    categories,
  } = useTransactionStore();

  const [filters, setFilters] = useState<TransactionFilters>({});
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);

  useEffect(() => {
    listTransactions(filters);
    getTransactionSummary();
    listCategories();
  }, [filters, listTransactions, getTransactionSummary, listCategories]);

  /**
   * 处理删除收支记录
   */
  const handleDelete = async (transactionId: number) => {
    try {
      await deleteTransaction(transactionId);
      message.success('收支记录删除成功');
      getTransactionSummary();
    } catch {
      message.error('收支记录删除失败');
    }
  };

  /**
   * 处理编辑收支记录
   */
  const handleEdit = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setIsModalOpen(true);
  };

  /**
   * 处理新增收支记录
   */
  const handleAdd = () => {
    setEditingTransaction(null);
    setIsModalOpen(true);
  };

  /**
   * 处理表单提交成功
   */
  const handleFormSuccess = () => {
    setIsModalOpen(false);
    setEditingTransaction(null);
    listTransactions(filters);
    getTransactionSummary();
  };

  /**
   * 处理筛选条件变化
   */
  const handleFilterChange = (key: keyof TransactionFilters, value: unknown) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
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
  };

  /**
   * 处理分页变化
   */
  const handlePageChange = (newPage: number, newPageSize: number) => {
    setFilters((prev) => ({ ...prev, page: newPage, page_size: newPageSize }));
  };

  /**
   * 重置筛选条件
   */
  const handleReset = () => {
    setFilters({});
  };

  const columns: ColumnsType<Transaction> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      width: 80,
      render: (type: string) => (
        <Tag color={getTransactionTypeColor(type)}>{getTransactionTypeLabel(type)}</Tag>
      ),
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 120,
    },
    {
      title: '金额',
      dataIndex: 'amount',
      key: 'amount',
      width: 120,
      render: (amount: string, record) => (
        <span
          className="font-medium"
          style={{ color: record.type === 'income' ? '#52c41a' : '#f5222d' }}
        >
          {record.type === 'income' ? '+' : '-'}¥{parseFloat(amount).toFixed(2)}
        </span>
      ),
    },
    {
      title: '关联订单',
      dataIndex: 'order_id',
      key: 'order_id',
      width: 100,
      render: (orderId: number | null) => (orderId ? `#${orderId}` : '-'),
    },
    {
      title: '备注',
      dataIndex: 'note',
      key: 'note',
      width: 200,
      ellipsis: true,
      render: (note: string | null) => note || '-',
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm:ss'),
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除此收支记录吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="p-6">
      <Row gutter={16} className="mb-4">
        <Col span={8}>
          <Card>
            <Statistic
              title="总收入"
              value={summary?.income || 0}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
              prefix={<ArrowUpOutlined />}
              suffix="元"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="总支出"
              value={summary?.expense || 0}
              precision={2}
              valueStyle={{ color: '#cf1322' }}
              prefix={<ArrowDownOutlined />}
              suffix="元"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="净利润"
              value={summary?.net_profit || 0}
              precision={2}
              valueStyle={{ color: (summary?.net_profit || 0) >= 0 ? '#3f8600' : '#cf1322' }}
              prefix="¥"
              suffix="元"
            />
          </Card>
        </Col>
      </Row>

      <Card
        title="收支记录"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新增记录
          </Button>
        }
      >
        <div className="mb-4">
          <Space size="middle" wrap>
            <RangePicker
              placeholder={['开始日期', '结束日期']}
              onChange={handleDateRangeChange}
            />
            <Select
              placeholder="类型"
              allowClear
              style={{ width: 120 }}
              value={filters.type}
              onChange={(value) => handleFilterChange('type', value)}
              options={TRANSACTION_TYPE_OPTIONS.map((opt) => ({
                value: opt.value,
                label: opt.label,
              }))}
            />
            <Select
              placeholder="分类"
              allowClear
              style={{ width: 150 }}
              value={filters.category}
              onChange={(value) => handleFilterChange('category', value)}
              options={categories.map((c) => ({ value: c.name, label: c.name }))}
            />
            <Button icon={<ReloadOutlined />} onClick={handleReset}>
              重置
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={transactions}
          rowKey="id"
          loading={isLoading}
          pagination={false}
          scroll={{ x: 1000 }}
        />

        <div className="mt-4 flex justify-end">
          <Pagination
            current={page}
            pageSize={pageSize}
            total={total}
            showSizeChanger
            showQuickJumper
            showTotal={(total) => `共 ${total} 条`}
            onChange={handlePageChange}
            onShowSizeChange={handlePageChange}
          />
        </div>
      </Card>

      <Modal
        title={editingTransaction ? '编辑收支记录' : '新增收支记录'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingTransaction(null);
        }}
        footer={null}
        width={600}
        destroyOnHidden
      >
        <TransactionForm
          transaction={editingTransaction}
          onSuccess={handleFormSuccess}
          onCancel={() => {
            setIsModalOpen(false);
            setEditingTransaction(null);
          }}
        />
      </Modal>
    </div>
  );
};

export default TransactionListPage;
