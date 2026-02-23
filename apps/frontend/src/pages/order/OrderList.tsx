/**
 * Dot-Store V2.2 订单列表页面
 * 移动端使用卡片式布局，桌面端使用表格布局
 * 遵循设计规范：触摸目标≥44px，按钮高度≥48px
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
  List,
  Typography,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  SearchOutlined,
  ReloadOutlined,
  StopOutlined,
  EyeOutlined,
  DollarOutlined,
  CalendarOutlined,
  TagOutlined,
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
  getPaymentMethodLabel,
} from '@/types/order';
import OrderForm from './OrderForm';
import { orderService } from '@/services/orderService';

import { eventService } from '@/services/eventService';
import type { BusinessEvent } from '@/types/event';

import { EVENT_CATEGORY_COLORS, EVENT_CATEGORY_LABELS } from '@/types/event';

import { EVENT_TYPE_LABELS } from '@/types/event';

const { RangePicker } = DatePicker;
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
 * 获取状态标签颜色
 */
const getStatusColor = (status: string): string => {
  const colorMap: Record<string, string> = {
    completed: '#52C41A',
    voided: '#F5222D',
    cancelled: '#FA541C',
  };
  return colorMap[status] || '#6B7280';
};

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
  const isMobile = useIsMobile();

  useEffect(() => {
    listOrders(filters);
    listCategories();
  }, [filters, listOrders, listCategories]);

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

  /**
   * 渲染移动端订单卡片
   */
  const renderMobileOrderCard = (order: Order) => {
    const category = categories.find((c) => c.id === order.category_id);
    
    return (
      <Card
        key={order.id}
        style={{ marginBottom: 12, borderRadius: 8 }}
        styles={{ body: { padding: 12 } }}
        onClick={() => handleViewDetail(order)}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <div>
            <Text strong style={{ fontSize: 14, color: '#3B82F6' }}>
              {order.order_no || '-'}
            </Text>
            <div style={{ marginTop: 4 }}>
              <Tag color={order.status === 'completed' ? 'green' : order.status === 'voided' ? 'red' : 'orange'}>
                {getOrderStatusLabel(order.status)}
              </Tag>
              <Tag color="blue" style={{ marginLeft: 4 }}>
                {getOrderTypeLabel(order.order_type)}
              </Tag>
            </div>
          </div>
          <Text strong style={{ fontSize: 18, color: '#52C41A' }}>
            ¥{parseFloat(order.amount).toFixed(2)}
          </Text>
        </div>
        
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 8, fontSize: 12, color: '#6B7280' }}>
          <span>
            <CalendarOutlined style={{ marginRight: 4 }} />
            {dayjs(order.created_at).format('MM-DD HH:mm')}
          </span>
          {order.payment_method && (
            <span>
              <DollarOutlined style={{ marginRight: 4 }} />
              {getPaymentMethodLabel(order.payment_method)}
            </span>
          )}
          {category && (
            <span>
              <TagOutlined style={{ marginRight: 4 }} />
              {category.name}
            </span>
          )}
        </div>
        
        {order.tags && order.tags.length > 0 && (
          <div style={{ marginBottom: 8 }}>
            {order.tags.map((tag) => (
              <Tag key={tag} style={{ marginBottom: 4, fontSize: 11 }}>
                {tag}
              </Tag>
            ))}
          </div>
        )}
        
        <div style={{ display: 'flex', gap: 8, marginTop: 8, paddingTop: 8, borderTop: '1px solid #F3F4F6' }}>
          <Button
            type="primary"
            size="small"
            icon={<EyeOutlined />}
            onClick={(e) => {
              e.stopPropagation();
              handleViewDetail(order);
            }}
            style={{ flex: 1, height: TOUCH_TARGET_MIN }}
          >
            详情
          </Button>
          <Button
            size="small"
            icon={<EditOutlined />}
            onClick={(e) => {
              e.stopPropagation();
              handleEdit(order);
            }}
            disabled={order.status === 'voided'}
            style={{ flex: 1, height: TOUCH_TARGET_MIN }}
          >
            编辑
          </Button>
          {order.status !== 'voided' && (
            <Button
              size="small"
              danger
              icon={<StopOutlined />}
              onClick={(e) => {
                e.stopPropagation();
                setVoidModal({ visible: true, orderId: order.id, reason: '' });
              }}
              style={{ flex: 1, height: TOUCH_TARGET_MIN }}
            >
              作废
            </Button>
          )}
        </div>
      </Card>
    );
  };

  /**
   * 桌面端表格列定义
   */
  const columns: ColumnsType<Order> = [
    {
      title: '订单编号',
      dataIndex: 'order_no',
      key: 'order_no',
      width: 150,
      render: (orderNo: string) => (
        <span style={{ fontFamily: 'monospace', color: '#3B82F6' }}>{orderNo || '-'}</span>
      ),
    },
    {
      title: '金额',
      dataIndex: 'amount',
      key: 'amount',
      width: 120,
      render: (amount: string) => (
        <span style={{ color: '#52C41A', fontWeight: 500 }}>¥{parseFloat(amount).toFixed(2)}</span>
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
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>{getOrderStatusLabel(status)}</Tag>
      ),
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

  /**
   * 渲染移动端筛选区域
   */
  const renderMobileFilters = () => (
    <div style={{ padding: '12px 16px', background: '#fff', marginBottom: 12 }}>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8, flexWrap: 'wrap' }}>
        <Select
          placeholder="类型"
          allowClear
          style={{ flex: '1 1 45%', minWidth: 100 }}
          value={filters.order_type}
          onChange={(value) => handleFilterChange('order_type', value)}
          options={ORDER_TYPE_OPTIONS}
        />
        <Select
          placeholder="状态"
          allowClear
          style={{ flex: '1 1 45%', minWidth: 100 }}
          value={filters.status}
          onChange={(value) => handleFilterChange('status', value)}
          options={ORDER_STATUS_OPTIONS}
        />
      </div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <RangePicker
          style={{ flex: 1 }}
          placeholder={['开始', '结束']}
          onChange={handleDateRangeChange}
          size="small"
        />
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <Input
          placeholder="标签搜索"
          prefix={<SearchOutlined />}
          style={{ flex: 1 }}
          value={filters.tags as string}
          onChange={(e) => handleFilterChange('tags', e.target.value)}
        />
        <Button icon={<ReloadOutlined />} onClick={handleReset} style={{ minWidth: TOUCH_TARGET_MIN }}>
          重置
        </Button>
      </div>
    </div>
  );

  /**
   * 渲染桌面端筛选区域
   */
  const renderDesktopFilters = () => (
    <div style={{ marginBottom: 16 }}>
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
          value={filters.tags as string}
          onChange={(e) => handleFilterChange('tags', e.target.value)}
        />
        <Button icon={<ReloadOutlined />} onClick={handleReset}>
          重置
        </Button>
      </Space>
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
        <Text strong style={{ fontSize: isMobile ? 16 : 20 }}>订单管理</Text>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={handleAdd}
          style={{ height: isMobile ? TOUCH_TARGET_MIN : 32 }}
        >
          新增订单
        </Button>
      </div>

      {/* 筛选区域 */}
      {isMobile ? renderMobileFilters() : renderDesktopFilters()}

      {/* 订单列表 */}
      {isMobile ? (
        <List
          dataSource={orders}
          loading={isLoading}
          renderItem={renderMobileOrderCard}
          locale={{ emptyText: '暂无订单记录' }}
        />
      ) : (
        <Card>
          <Table
            columns={columns}
            dataSource={orders}
            rowKey="id"
            loading={isLoading}
            pagination={false}
            scroll={{ x: 1200 }}
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
          onChange={handlePageChange}
          onShowSizeChange={handlePageChange}
          simple={isMobile}
          size={isMobile ? 'small' : 'default'}
        />
      </div>

      {/* 新增/编辑订单弹窗 */}
      <Modal
        title={editingOrder ? '编辑订单' : '新增订单'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingOrder(null);
        }}
        footer={null}
        width={isMobile ? '100%' : 600}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
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

      {/* 订单详情弹窗 */}
      <Modal
        title="订单详情"
        open={!!detailModal}
        onCancel={() => {
          setDetailModal(null);
          setOrderItems([]);
          setOrderEvents([]);
        }}
        footer={null}
        width={isMobile ? '100%' : 800}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        {detailModal && (
          <div>
            <Descriptions column={isMobile ? 1 : 2} bordered size="small">
              <Descriptions.Item label="订单编号">{detailModal.order_no}</Descriptions.Item>
              <Descriptions.Item label="金额">
                <span style={{ color: '#52C41A', fontWeight: 500 }}>¥{parseFloat(detailModal.amount).toFixed(2)}</span>
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
              <Descriptions.Item label="备注" span={isMobile ? 1 : 2}>
                {detailModal.note || '-'}
              </Descriptions.Item>
            </Descriptions>

            {orderItems.length > 0 && (
              <>
                <Divider>订单项</Divider>
                <List
                  dataSource={orderItems}
                  renderItem={(item) => (
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      padding: '8px 0',
                      borderBottom: '1px solid #F3F4F6'
                    }}>
                      <div>
                        <Text strong>{item.product_name}</Text>
                        <Text type="secondary" style={{ marginLeft: 8 }}>x{item.quantity}</Text>
                      </div>
                      <Text>¥{parseFloat(item.amount).toFixed(2)}</Text>
                    </div>
                  )}
                />
              </>
            )}

            {orderEvents.length > 0 && (
              <>
                <Divider>操作日志</Divider>
                <List
                  size="small"
                  dataSource={orderEvents}
                  renderItem={(event) => (
                    <div style={{ padding: '8px 0', borderBottom: '1px solid #F3F4F6' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          {dayjs(event.created_at).format('MM-DD HH:mm:ss')}
                        </Text>
                        <Tag color={EVENT_CATEGORY_COLORS[event.event_category as keyof typeof EVENT_CATEGORY_COLORS]} style={{ fontSize: 11 }}>
                          {EVENT_CATEGORY_LABELS[event.event_category as keyof typeof EVENT_CATEGORY_LABELS]}
                        </Tag>
                      </div>
                      <Text style={{ fontSize: 13 }}>
                        {EVENT_TYPE_LABELS[event.event_type as keyof typeof EVENT_TYPE_LABELS] || event.event_type}
                      </Text>
                    </div>
                  )}
                />
              </>
            )}
          </div>
        )}
      </Modal>

      {/* 作废订单弹窗 */}
      <Modal
        title="作废订单"
        open={voidModal.visible}
        onCancel={() => setVoidModal({ visible: false, orderId: null, reason: '' })}
        onOk={handleVoid}
        okText="确定作废"
        cancelText="取消"
      >
        <div style={{ padding: '16px 0' }}>
          <p style={{ marginBottom: 12, color: '#6B7280' }}>请输入作废原因：</p>
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
