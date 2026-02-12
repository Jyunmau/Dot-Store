/**
 * 订单回收站页面
 */
import React, { useEffect } from 'react';
import { Table, Button, Space, Tag, message, Popconfirm, Card, Pagination, Empty } from 'antd';
import { UndoOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useOrderStore } from '@/store/orderStore';
import type { Order } from '@/types/order';
import { getOrderTypeLabel, getOrderStatusLabel } from '@/types/order';

/**
 * 订单回收站页面组件
 */
const OrderRecyclePage: React.FC = () => {
  const {
    recycleOrders,
    total,
    page,
    pageSize,
    isLoading,
    getRecycleOrders,
    restoreOrder,
    categories,
    listCategories,
  } = useOrderStore();

  useEffect(() => {
    getRecycleOrders();
    listCategories();
  }, [getRecycleOrders, listCategories]);

  /**
   * 处理恢复订单
   */
  const handleRestore = async (orderId: number) => {
    try {
      await restoreOrder(orderId);
      message.success('订单恢复成功');
    } catch {
      message.error('订单恢复失败');
    }
  };

  /**
   * 处理分页变化
   */
  const handlePageChange = (newPage: number, newPageSize: number) => {
    getRecycleOrders(newPage, newPageSize);
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
      title: '删除时间',
      dataIndex: 'deleted_at',
      key: 'deleted_at',
      width: 180,
      render: (date: string) => (date ? dayjs(date).format('YYYY-MM-DD HH:mm:ss') : '-'),
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Popconfirm
            title="确定要恢复此订单吗？"
            onConfirm={() => handleRestore(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" size="small" icon={<UndoOutlined />}>
              恢复
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="p-6">
      <Card title="订单回收站">
        {recycleOrders.length === 0 && !isLoading ? (
          <Empty description="回收站为空" />
        ) : (
          <>
            <Table
              columns={columns}
              dataSource={recycleOrders}
              rowKey="id"
              loading={isLoading}
              pagination={false}
              scroll={{ x: 800 }}
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
          </>
        )}
      </Card>
    </div>
  );
};

export default OrderRecyclePage;
