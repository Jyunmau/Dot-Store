/**
 * Dot-Store V2.2 事件日志页面
 */
import React, { useState, useEffect } from 'react';
import { Table, Card, DatePicker, Select, Tag, Space, Descriptions, Modal, Button, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { eventService } from '../../services/eventService';
import type { BusinessEvent, EventCategory } from '../../types/event';
import { EVENT_CATEGORY_COLORS, EVENT_CATEGORY_LABELS, EVENT_TYPE_LABELS } from '../../types/event';

const { RangePicker } = DatePicker;
const { Title } = Typography;

const EventLog: React.FC = () => {
  const [events, setEvents] = useState<BusinessEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<EventCategory | undefined>();
  const [detailModal, setDetailModal] = useState<BusinessEvent | null>(null);

  /**
   * 获取事件列表
   */
  const fetchEvents = async () => {
    setLoading(true);
    try {
      const params: any = { page, page_size: pageSize };
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
   * 表格列定义
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
      render: (type: string) => {
        const labels: Record<string, string> = {
          user: '用户',
          system: '系统',
          mcp: 'MCP',
        };
        return labels[type] || type;
      },
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
    <Card>
      <Title level={4} style={{ marginBottom: 16 }}>事件日志</Title>
      
      <Space style={{ marginBottom: 16 }}>
        <RangePicker
          value={dateRange}
          onChange={(dates) => setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs] | null)}
          placeholder={['开始日期', '结束日期']}
        />
        <Select
          style={{ width: 120 }}
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

      <Table
        columns={columns}
        dataSource={events}
        rowKey="id"
        loading={loading}
        pagination={{
          current: page,
          pageSize,
          total,
          showSizeChanger: true,
          showTotal: (total) => `共 ${total} 条`,
          onChange: (p, ps) => {
            setPage(p);
            setPageSize(ps);
          },
        }}
      />

      <Modal
        title="事件详情"
        open={!!detailModal}
        onCancel={() => setDetailModal(null)}
        footer={null}
        width={600}
      >
        {detailModal && (
          <Descriptions column={1} bordered>
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
            <Descriptions.Item label="操作人类型">{detailModal.operator_type}</Descriptions.Item>
            <Descriptions.Item label="IP地址">{detailModal.ip_address || '-'}</Descriptions.Item>
            <Descriptions.Item label="创建时间">
              {dayjs(detailModal.created_at).format('YYYY-MM-DD HH:mm:ss')}
            </Descriptions.Item>
            {detailModal.data && (
              <Descriptions.Item label="事件数据">
                <pre style={{ margin: 0, maxHeight: 200, overflow: 'auto' }}>
                  {JSON.stringify(detailModal.data, null, 2)}
                </pre>
              </Descriptions.Item>
            )}
          </Descriptions>
        )}
      </Modal>
    </Card>
  );
};

export default EventLog;
