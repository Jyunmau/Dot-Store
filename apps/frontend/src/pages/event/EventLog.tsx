/**
 * Dot-Store V2.2 事件日志页面
 * 移动端使用卡片式布局，桌面端使用表格布局
 * 遵循设计规范：触摸目标≥44px，按钮高度≥48px
 */
import React, { useState, useEffect } from 'react';
import { Table, Card, DatePicker, Select, Tag, Space, Descriptions, Modal, Button, Typography, List, Pagination } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { eventService } from '../../services/eventService';
import type { BusinessEvent, EventCategory } from '../../types/event';
import { EVENT_CATEGORY_COLORS, EVENT_CATEGORY_LABELS, EVENT_TYPE_LABELS } from '../../types/event';

const { RangePicker } = DatePicker;
const { Text, Title } = Typography;

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
 * 获取操作人类型标签
 */
const getOperatorTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    user: '用户',
    system: '系统',
    mcp: 'MCP',
  };
  return labels[type] || type;
};

/**
 * 事件日志页面组件
 */
const EventLog: React.FC = () => {
  const [events, setEvents] = useState<BusinessEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<EventCategory | undefined>();
  const [detailModal, setDetailModal] = useState<BusinessEvent | null>(null);
  const isMobile = useIsMobile();

  /**
   * 获取事件列表
   */
  const fetchEvents = async () => {
    setLoading(true);
    try {
      const params: Record<string, unknown> = { page, page_size: pageSize };
      if (dateRange) {
        params.start_date = dateRange[0].format('YYYY-MM-DD');
        params.end_date = dateRange[1].add(1, 'day').format('YYYY-MM-DD');
      }
      if (categoryFilter) {
        params.event_category = categoryFilter;
      }
      const response = await eventService.getEvents(params);
      setEvents(response.items);
      setTotal(response.total);
    } catch (error) {
      console.error('获取事件列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [page, pageSize, dateRange, categoryFilter]);

  /**
   * 渲染移动端事件卡片
   */
  const renderMobileEventCard = (event: BusinessEvent) => (
    <Card
      key={event.id}
      style={{ marginBottom: 12, borderRadius: 8 }}
      styles={{ body: { padding: 12 } }}
      onClick={() => setDetailModal(event)}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <Tag color={EVENT_CATEGORY_COLORS[event.event_category]}>
          {EVENT_CATEGORY_LABELS[event.event_category]}
        </Tag>
        <Text type="secondary" style={{ fontSize: 12 }}>
          {dayjs(event.created_at).format('MM-DD HH:mm')}
        </Text>
      </div>
      
      <Text strong style={{ fontSize: 14, display: 'block', marginBottom: 8 }}>
        {EVENT_TYPE_LABELS[event.event_type as keyof typeof EVENT_TYPE_LABELS] || event.event_type}
      </Text>
      
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, fontSize: 12, color: '#6B7280' }}>
        {event.entity_type && event.entity_id && (
          <span>
            {event.entity_type}#{event.entity_id}
          </span>
        )}
        <span>
          {getOperatorTypeLabel(event.operator_type)}
        </span>
        {event.ip_address && (
          <span>
            IP: {event.ip_address}
          </span>
        )}
      </div>
      
      <div style={{ marginTop: 8, paddingTop: 8, borderTop: '1px solid #F3F4F6' }}>
        <Button
          type="link"
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            setDetailModal(event);
          }}
          style={{ padding: 0, height: TOUCH_TARGET_MIN }}
        >
          查看详情
        </Button>
      </div>
    </Card>
  );

  /**
   * 桌面端表格列定义
   */
  const columns: ColumnsType<BusinessEvent> = [
    {
      title: '时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (text: string) => dayjs(text).format('YYYY-MM-DD HH:mm:ss'),
    },
    {
      title: '分类',
      dataIndex: 'event_category',
      key: 'event_category',
      width: 100,
      render: (category: EventCategory) => (
        <Tag color={EVENT_CATEGORY_COLORS[category]}>
          {EVENT_CATEGORY_LABELS[category]}
        </Tag>
      ),
    },
    {
      title: '事件类型',
      dataIndex: 'event_type',
      key: 'event_type',
      width: 150,
      render: (type: string) => EVENT_TYPE_LABELS[type as keyof typeof EVENT_TYPE_LABELS] || type,
    },
    {
      title: '实体',
      key: 'entity',
      width: 150,
      render: (_, record) => {
        if (record.entity_type && record.entity_id) {
          return `${record.entity_type}#${record.entity_id}`;
        }
        return '-';
      },
    },
    {
      title: '操作人类型',
      dataIndex: 'operator_type',
      key: 'operator_type',
      width: 100,
      render: (type: string) => getOperatorTypeLabel(type),
    },
    {
      title: 'IP地址',
      dataIndex: 'ip_address',
      key: 'ip_address',
      width: 140,
      render: (ip: string) => ip || '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_, record) => (
        <Button type="link" onClick={() => setDetailModal(record)}>
          详情
        </Button>
      ),
    },
  ];

  return (
    <div style={{ padding: isMobile ? '12px' : '24px', background: isMobile ? '#F9FAFB' : 'transparent' }}>
      {/* 页面标题 */}
      <div style={{ 
        marginBottom: isMobile ? 0 : 16,
        padding: isMobile ? '12px 16px' : 0,
        background: isMobile ? '#fff' : 'transparent',
      }}>
        <Title level={4} style={{ margin: 0 }}>事件日志</Title>
      </div>

      {/* 筛选区域 */}
      <div style={{ 
        marginBottom: 16, 
        padding: isMobile ? '12px 16px' : 0,
        background: isMobile ? '#fff' : 'transparent',
      }}>
        <Space style={{ width: isMobile ? '100%' : 'auto' }} direction={isMobile ? 'vertical' : 'horizontal'} size="middle">
          <RangePicker
            value={dateRange}
            onChange={(dates) => setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs] | null)}
            placeholder={['开始日期', '结束日期']}
            style={{ width: isMobile ? '100%' : 'auto' }}
          />
          <Select
            style={{ width: isMobile ? '100%' : 120 }}
            placeholder="事件分类"
            allowClear
            value={categoryFilter}
            onChange={setCategoryFilter}
          >
            {Object.entries(EVENT_CATEGORY_LABELS).map(([key, label]) => (
              <Select.Option key={key} value={key}>
                {label}
              </Select.Option>
            ))}
          </Select>
        </Space>
      </div>

      {/* 事件列表 */}
      {isMobile ? (
        <List
          dataSource={events}
          loading={loading}
          renderItem={renderMobileEventCard}
          locale={{ emptyText: '暂无事件记录' }}
        />
      ) : (
        <Card>
          <Table
            columns={columns}
            dataSource={events}
            rowKey="id"
            loading={loading}
            pagination={false}
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
          showTotal={(total) => `共 ${total} 条`}
          onChange={(p, ps) => {
            setPage(p);
            setPageSize(ps);
          }}
          simple={isMobile}
          size={isMobile ? 'small' : 'default'}
        />
      </div>

      {/* 事件详情弹窗 */}
      <Modal
        title="事件详情"
        open={!!detailModal}
        onCancel={() => setDetailModal(null)}
        footer={null}
        width={isMobile ? '100%' : 600}
        style={isMobile ? { top: 0, margin: 0, maxWidth: '100vw' } : {}}
      >
        {detailModal && (
          <Descriptions column={isMobile ? 1 : 2} bordered size="small">
            <Descriptions.Item label="事件ID">{detailModal.id}</Descriptions.Item>
            <Descriptions.Item label="事件类型">
              {EVENT_TYPE_LABELS[detailModal.event_type as keyof typeof EVENT_TYPE_LABELS] || detailModal.event_type}
            </Descriptions.Item>
            <Descriptions.Item label="事件分类">
              <Tag color={EVENT_CATEGORY_COLORS[detailModal.event_category]}>
                {EVENT_CATEGORY_LABELS[detailModal.event_category]}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="实体">
              {detailModal.entity_type && detailModal.entity_id
                ? `${detailModal.entity_type}#${detailModal.entity_id}`
                : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="操作人ID">{detailModal.operator_id}</Descriptions.Item>
            <Descriptions.Item label="操作人类型">{getOperatorTypeLabel(detailModal.operator_type)}</Descriptions.Item>
            <Descriptions.Item label="IP地址">{detailModal.ip_address || '-'}</Descriptions.Item>
            <Descriptions.Item label="创建时间">
              {dayjs(detailModal.created_at).format('YYYY-MM-DD HH:mm:ss')}
            </Descriptions.Item>
            {detailModal.data && (
              <Descriptions.Item label="事件数据" span={isMobile ? 1 : 2}>
                <pre style={{ margin: 0, maxHeight: 200, overflow: 'auto', fontSize: 12 }}>
                  {JSON.stringify(detailModal.data, null, 2)}
                </pre>
              </Descriptions.Item>
            )}
          </Descriptions>
        )}
      </Modal>
    </div>
  );
};

export default EventLog;
