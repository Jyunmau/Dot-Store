/**
 * Dot-Store V2.2 订单列表页面
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
  Descriptions,
  Divider,
  InputNumber,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SearchOutlined,
  ReloadOutlined,
  StopOutlined,
  EyeOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useOrderStore } from '@/store/orderStore';
import type { Order, OrderItem, OrderFilters, OrderDetail } from '@/types/order';
import { 
  getOrderTypeLabel, 
  getOrderStatusLabel, 
  ORDER_TYPE_OPTIONS, 
  ORDER_STATUS_OPTIONS,
  PAYMENT_METHOD_OPTIONS,
  getPaymentMethodLabel,
} from '@/types/order';
import OrderForm from './OrderForm';
import { orderService } from '@/services/orderService';

import { eventService } from '@/services/eventService';
import type { BusinessEvent } from '@/types/event';

import { EVENT_CATEGORY_COLORS, EVENT_CATEGORY_LABELS } from '@/types/event';

import { EVENT_TYPE_LABELS } from '@/types/event';

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
  const [detailModal, setDetailModal] = useState<OrderDetail | null>(null);
  const [orderItems, setOrderItems] = useState<OrderItem[]>([]);
  const [orderEvents, setOrderEvents] = useState<BusinessEvent[]>([]);
  const [voidModal, setVoidModal] = useState<{ visible: boolean; orderId: number | null; reason: string }>({
    visible: false,
    orderId: null,
    reason: '',
  });

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

  /**
   * 查看订单详情
   */
  const handleViewDetail = async (order: Order) => {
    try {
      const detail = await orderService.getOrder(order.id);
      setDetailModal(detail);
      setOrderItems(detail.items || []);
      
      const events = await eventService.getEntityEvents('order', order.id);
      setOrderEvents(events);
    } catch (error) {
      message.error('获取订单详情失败');
    }
  };

  /**
   * 作废订单
   */
  const handleVoid = async () => {
    if (!voidModal.orderId || !voidModal.reason.trim()) {
      message.warning('请输入作废原因');
      return;
    }
    
    try {
      await orderService.voidOrder(voidModal.orderId, voidModal.reason);
      message.success('订单作废成功');
      setVoidModal({ visible: false, orderId: null, reason: '' });
      listOrders(filters);
    } catch (error) {
      message.error('订单作废失败');
    }
  };

  const columns: ColumnsType<Order> = [
    {
      title: '订单编号',
      dataIndex: 'order_no',
      key: 'order_no',
      width: 150,
      render: (orderNo: string) => (
        <span className="font-mono text-blue-600">{orderNo || '-'}</span>
      ),
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
      title: '支付方式',
      dataIndex: 'payment_method',
      key: 'payment_method',
      width: 100,
      render: (method: string) => method ? (
        <Tag color="purple">{getPaymentMethodLabel(method)}</Tag>
      ) : '-',
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
          completed: 'green',
          voided: 'red',
          cancelled: 'orange',
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
      width: 200,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewDetail(record)}
          >
            详情
          </Button>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
            disabled={record.status === 'voided'}
          >
            编辑
          </Button>
          {record.status !== 'voided' && (
            <Popconfirm
              title="确定要作废此订单吗？"
              description="作废后无法恢复"
              onConfirm={() => setVoidModal({ visible: true, orderId: record.id, reason: '' })}
              okText="确定"
              cancelText="取消"
            >
              <Button type="link" size="small" danger icon={<StopOutlined />}>
                作废
              </Button>
            </Popconfirm>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div className="p-4 md:p-6">
      <Card 
        title="订单管理" 
        extra={
          <Space>
            <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
              新增订单
            </Button>
          </Space>
        }
      >
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
          scroll={{ x: 1200 }}
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

      <Modal
        title="订单详情"
        open={!!detailModal}
        onCancel={() => {
          setDetailModal(null);
          setOrderItems([]);
          setOrderEvents([]);
        }}
        footer={null}
        width={800}
      >
        {detailModal && (
          <div>
            <Descriptions column={2} bordered>
              <Descriptions.Item label="订单编号">{detailModal.order_no}</Descriptions.Item>
              <Descriptions.Item label="金额">
                <span className="text-green-600 font-medium">¥{parseFloat(detailModal.amount).toFixed(2)}</span>
              </Descriptions.Item>
              <Descriptions.Item label="订单类型">
                <Tag color="blue">{getOrderTypeLabel(detailModal.order_type)}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="支付方式">
                {detailModal.payment_method ? (
                  <Tag color="purple">{getPaymentMethodLabel(detailModal.payment_method)}</Tag>
                ) : '-'}
              </Descriptions.Item>
              <Descriptions.Item label="状态">
                <Tag color={detailModal.status === 'completed' ? 'green' : 'red'}>
                  {getOrderStatusLabel(detailModal.status)}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="创建时间">
                {dayjs(detailModal.created_at).format('YYYY-MM-DD HH:mm:ss')}
              </Descriptions.Item>
              <Descriptions.Item label="备注" span={2}>
                {detailModal.note || '-'}
              </Descriptions.Item>
            </Descriptions>

            {orderItems.length > 0 && (
              <>
                <Divider>订单项</Divider>
                <Table
                  dataSource={orderItems}
                  rowKey="id"
                  pagination={false}
                  size="small"
                  columns={[
                    { title: '产品名称', dataIndex: 'product_name', key: 'product_name' },
                    { title: '数量', dataIndex: 'quantity', key: 'quantity' },
                    { title: '单价', dataIndex: 'unit_price', key: 'unit_price', render: (v: string) => `¥${parseFloat(v).toFixed(2)}` },
                    { title: '金额', dataIndex: 'amount', key: 'amount', render: (v: string) => `¥${parseFloat(v).toFixed(2)}` },
                  ]}
                />
              </>
            )}

            {orderEvents.length > 0 && (
              <>
                <Divider>操作日志</Divider>
                <Table
                  dataSource={orderEvents}
                  rowKey="id"
                  pagination={false}
                  size="small"
                  columns={[
                    { 
                      title: '时间', 
                      dataIndex: 'created_at', 
                      key: 'created_at',
                      render: (v: string) => dayjs(v).format('YYYY-MM-DD HH:mm:ss'),
                    },
                    { 
                      title: '事件类型', 
                      dataIndex: 'event_type', 
                      key: 'event_type',
                      render: (type: string) => EVENT_TYPE_LABELS[type as keyof typeof EVENT_TYPE_LABELS] || type,
                    },
                    { 
                      title: '分类', 
                      dataIndex: 'event_category', 
                      key: 'event_category',
                      render: (category: string) => (
                        <Tag color={EVENT_CATEGORY_COLORS[category as keyof typeof EVENT_CATEGORY_COLORS]}>
                          {EVENT_CATEGORY_LABELS[category as keyof typeof EVENT_CATEGORY_LABELS]}
                        </Tag>
                      ),
                    },
                    { 
                      title: '数据', 
                      dataIndex: 'data', 
                      key: 'data',
                      render: (data: Record<string, unknown>) => (
                        <pre className="text-xs">{JSON.stringify(data, null, 2)}</pre>
                      ),
                    },
                  ]}
                />
              </>
            )}
          </div>
        )}
      </Modal>

      <Modal
        title="作废订单"
        open={voidModal.visible}
        onCancel={() => setVoidModal({ visible: false, orderId: null, reason: '' })}
        onOk={handleVoid}
        okText="确定作废"
        cancelText="取消"
      >
        <div className="py-4">
          <p className="mb-4 text-gray-600">请输入作废原因：</p>
          <Input.TextArea
            value={voidModal.reason}
            onChange={(e) => setVoidModal({ ...voidModal, reason: e.target.value })}
            placeholder="请输入作废原因"
            rows={3}
          />
        </div>
      </Modal>
    </div>
  );
};

export default OrderListPage;
