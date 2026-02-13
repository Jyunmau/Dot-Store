/**
 * 积分兑换页面
 */
import React, { useEffect, useState } from 'react';
import {
  Table,
  Button,
  Space,
  Modal,
  message,
  Card,
  Pagination,
  Form,
  InputNumber,
  Select,
} from 'antd';
import {
  SwapOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useMemberStore } from '@/store/memberStore';
import type { PointsExchange, PointsExchangeParams } from '@/types/member';

interface ExchangeFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

/**
 * 积分兑换表单组件
 */
const ExchangeForm: React.FC<ExchangeFormProps> = ({ onSuccess, onCancel }) => {
  const [form] = Form.useForm();
  const { exchangePoints, members } = useMemberStore();
  const [loading, setLoading] = useState(false);
  const [selectedMemberId, setSelectedMemberId] = useState<number | undefined>();

  const selectedMember = members.find((m) => m.id === selectedMemberId);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      await exchangePoints(values as PointsExchangeParams);
      message.success('积分兑换成功');
      onSuccess();
    } catch (error: unknown) {
      if (error instanceof Error) {
        message.error(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} layout="vertical" onFinish={handleSubmit}>
      <Form.Item
        name="member_id"
        label="会员"
        rules={[{ required: true, message: '请选择会员' }]}
      >
        <Select
          placeholder="请选择会员"
          showSearch
          optionFilterProp="label"
          onChange={(value) => setSelectedMemberId(value)}
          options={members.map((m) => ({
            value: m.id,
            label: `${m.name} (${m.phone}) - 积分: ${m.points}`,
          }))}
        />
      </Form.Item>
      {selectedMember && (
        <div className="mb-4 p-3 bg-gray-50 rounded">
          <span>当前积分：<strong className="text-orange-500">{selectedMember.points}</strong></span>
        </div>
      )}
      <Form.Item
        name="points"
        label="兑换积分"
        rules={[
          { required: true, message: '请输入兑换积分' },
          { type: 'number', min: 1, message: '积分必须大于0' },
        ]}
      >
        <InputNumber
          placeholder="请输入兑换积分"
          min={1}
          step={1}
          style={{ width: '100%' }}
          max={selectedMember?.points}
        />
      </Form.Item>
      <Form.Item
        name="amount"
        label="兑换金额（元）"
        rules={[
          { required: true, message: '请输入兑换金额' },
          { type: 'number', min: 0.01, message: '金额必须大于0' },
        ]}
      >
        <InputNumber
          placeholder="请输入兑换金额"
          min={0.01}
          step={0.01}
          precision={2}
          style={{ width: '100%' }}
          prefix="¥"
        />
      </Form.Item>
      <Form.Item className="mb-0 flex justify-end">
        <Space>
          <Button onClick={onCancel}>取消</Button>
          <Button type="primary" htmlType="submit" loading={loading}>
            确认兑换
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

/**
 * 积分兑换页面组件
 */
const PointsExchangePage: React.FC = () => {
  const {
    pointsExchanges,
    total,
    page,
    pageSize,
    isLoading,
    listMembers,
    getExchanges,
  } = useMemberStore();

  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    listMembers({ page_size: 100 });
    getExchanges(page, pageSize);
  }, [listMembers, getExchanges, page, pageSize]);

  /**
   * 处理分页变化
   */
  const handlePageChange = (newPage: number, newPageSize: number) => {
    getExchanges(newPage, newPageSize);
  };

  /**
   * 处理表单提交成功
   */
  const handleFormSuccess = () => {
    setIsModalOpen(false);
    getExchanges(page, pageSize);
    listMembers({ page_size: 100 });
  };

  const columns: ColumnsType<PointsExchange> = [
    {
      title: '兑换ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '会员',
      dataIndex: 'member_name',
      key: 'member_name',
      width: 150,
      render: (name: string | undefined, record) => name || `会员ID: ${record.member_id}`,
    },
    {
      title: '兑换积分',
      dataIndex: 'points',
      key: 'points',
      width: 120,
      render: (points: number) => (
        <span className="text-orange-500 font-medium">{points}</span>
      ),
    },
    {
      title: '兑换金额',
      dataIndex: 'amount',
      key: 'amount',
      width: 120,
      render: (amount: string) => (
        <span className="text-green-500 font-medium">¥{parseFloat(amount).toFixed(2)}</span>
      ),
    },
    {
      title: '兑换时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm:ss'),
    },
  ];

  return (
    <div className="p-6">
      <Card
        title="积分兑换"
        extra={
          <Button
            type="primary"
            icon={<SwapOutlined />}
            onClick={() => setIsModalOpen(true)}
          >
            积分兑换
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={pointsExchanges}
          rowKey="id"
          loading={isLoading}
          pagination={false}
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
        title="积分兑换"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        width={500}
        destroyOnHidden
      >
        <ExchangeForm
          onSuccess={handleFormSuccess}
          onCancel={() => setIsModalOpen(false)}
        />
      </Modal>
    </div>
  );
};

export default PointsExchangePage;
