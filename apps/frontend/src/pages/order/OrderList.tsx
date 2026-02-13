/**
 * 订单列表页面
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
  Input,
  Select,
  DatePicker,
  Pagination,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SearchOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useOrderStore } from '@/store/orderStore';
import type { Order, OrderFilters } from '@/types/order';
import { getOrderTypeLabel, getOrderStatusLabel, ORDER_TYPE_OPTIONS, ORDER_STATUS_OPTIONS } from '@/types/order';
import OrderForm from './OrderForm';

const { RangePicker } = DatePicker;

/**
 * 订单列表页面组件
 */
const OrderListPage: React.FC = () => {
  const {
    orders,
    total,
    page,
    pageSize,
    isLoading,
    listOrders,
    deleteOrder,
    listCategories,
    categories,
  } = useOrderStore();

  const [filters, setFilters] = useState<OrderFilters>({});
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingOrder, setEditingOrder] = useState<Order | null>(null);

  useEffect(() => {
    listOrders(filters);
    listCategories();
  }, [filters, listOrders, listCategories]);

  /**
   * 处理删除订单
   */
  const handleDelete = async (orderId: number) => {
    try {
      await deleteOrder(orderId);
      message.success('订单删除成功');
    } catch {
      message.error('订单删除失败');
    }
  };

  /**
   * 处理编辑订单
   */
  const handleEdit = (order: Order) => {
    setEditingOrder(order);
    setIsModalOpen(true);
  };

  /**
   * 处理新增订单
   */
  const handleAdd = () => {
    setEditingOrder(null);
    setIsModalOpen(true);
  };

  /**
   * 处理表单提交成功
   */
  const handleFormSuccess = () => {
    setIsModalOpen(false);
    setEditingOrder(null);
    listOrders(filters);
  };

  /**
   * 处理筛选条件变化
   */
  const handleFilterChange = (key: keyof OrderFilters, value: unknown) => {
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

  const columns: ColumnsType<Order> = [
    {
      title: '订单ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '金额',
      dataIndex: 'amount',
      key: 'amount',
      width: 120,
      render: (amount: string) => (
        <span className="text-green-600 font-medium">¥{parseFloat(amount).toFixed(2)}</span>
      ),
    },
    {
      title: '订单类型',
      dataIndex: 'order_type',
      key: 'order_type',
      width: 100,
      render: (type: string) => <Tag color="blue">{getOrderTypeLabel(type)}</Tag>,
    },
    {
      title: '分类',
      dataIndex: 'category_id',
      key: 'category_id',
      width: 100,
      render: (categoryId: number | null) => {
        const category = categories.find((c) => c.id === categoryId);
        return category ? category.name : '-';
      },
    },
    {
      title: '标签',
      dataIndex: 'tags',
      key: 'tags',
      width: 150,
      render: (tags: string[] | null) =>
        tags && tags.length > 0 ? (
          <Space size={[0, 4]} wrap>
            {tags.map((tag) => (
              <Tag key={tag} color="default">
                {tag}
              </Tag>
            ))}
          </Space>
        ) : (
          '-'
        ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => {
        const colorMap: Record<string, string> = {
          recorded: 'green',
          completed: 'blue',
          cancelled: 'red',
        };
        return <Tag color={colorMap[status] || 'default'}>{getOrderStatusLabel(status)}</Tag>;
      },
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
            title="确定要删除此订单吗？"
            description="删除后可在回收站恢复"
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
      <Card title="订单管理" extra={
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          新增订单
        </Button>
      }>
        <div className="mb-4">
          <Space size="middle" wrap>
            <RangePicker
              placeholder={['开始日期', '结束日期']}
              onChange={handleDateRangeChange}
            />
            <Select
              placeholder="订单类型"
              allowClear
              style={{ width: 120 }}
              value={filters.order_type}
              onChange={(value) => handleFilterChange('order_type', value)}
              options={ORDER_TYPE_OPTIONS}
            />
            <Select
              placeholder="订单状态"
              allowClear
              style={{ width: 120 }}
              value={filters.status}
              onChange={(value) => handleFilterChange('status', value)}
              options={ORDER_STATUS_OPTIONS}
            />
            <Select
              placeholder="分类"
              allowClear
              style={{ width: 150 }}
              value={filters.category_id}
              onChange={(value) => handleFilterChange('category_id', value)}
              options={categories.map((c) => ({ value: c.id, label: c.name }))}
            />
            <Input
              placeholder="标签搜索"
              prefix={<SearchOutlined />}
              style={{ width: 150 }}
              value={filters.tags}
              onChange={(e) => handleFilterChange('tags', e.target.value)}
            />
            <Button icon={<ReloadOutlined />} onClick={handleReset}>
              重置
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={orders}
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
        title={editingOrder ? '编辑订单' : '新增订单'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingOrder(null);
        }}
        footer={null}
        width={600}
        destroyOnHidden
      >
        <OrderForm
          order={editingOrder}
          onSuccess={handleFormSuccess}
          onCancel={() => {
            setIsModalOpen(false);
            setEditingOrder(null);
          }}
        />
      </Modal>
    </div>
  );
};

export default OrderListPage;
