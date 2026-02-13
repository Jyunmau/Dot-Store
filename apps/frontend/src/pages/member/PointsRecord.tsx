/**
 * 积分记录页面
 */
import React, { useEffect, useState } from 'react';
import {
  Table,
  Button,
  Space,
  Tag,
  Modal,
  message,
  Card,
  Select,
  Pagination,
  Form,
  InputNumber,
  Input,
} from 'antd';
import {
  PlusOutlined,
  MinusOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useMemberStore } from '@/store/memberStore';
import type { PointsRecord, PointsAddParams, PointsSubtractParams } from '@/types/member';
import { getPointsTypeLabel } from '@/types/member';

interface PointsFormProps {
  type: 'add' | 'subtract';
  onSuccess: () => void;
  onCancel: () => void;
}

/**
 * 积分表单组件
 */
const PointsForm: React.FC<PointsFormProps> = ({ type, onSuccess, onCancel }) => {
  const [form] = Form.useForm();
  const { addPoints, subtractPoints, members } = useMemberStore();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      if (type === 'add') {
        await addPoints(values as PointsAddParams);
        message.success('积分增加成功');
      } else {
        await subtractPoints(values as PointsSubtractParams);
        message.success('积分减少成功');
      }

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
          options={members.map((m) => ({
            value: m.id,
            label: `${m.name} (${m.phone}) - 积分: ${m.points}`,
          }))}
        />
      </Form.Item>
      <Form.Item
        name="points"
        label={type === 'add' ? '增加积分' : '减少积分'}
        rules={[
          { required: true, message: '请输入积分数量' },
          { type: 'number', min: 1, message: '积分必须大于0' },
        ]}
      >
        <InputNumber
          placeholder="请输入积分数量"
          min={1}
          step={1}
          style={{ width: '100%' }}
        />
      </Form.Item>
      <Form.Item
        name="reason"
        label="原因"
        rules={[{ required: true, message: '请输入原因' }]}
      >
        <Input.TextArea placeholder="请输入原因" rows={3} maxLength={256} showCount />
      </Form.Item>
      <Form.Item className="mb-0 flex justify-end">
        <Space>
          <Button onClick={onCancel}>取消</Button>
          <Button type="primary" htmlType="submit" loading={loading}>
            确认
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

/**
 * 积分记录页面组件
 */
const PointsRecordPage: React.FC = () => {
  const {
    members,
    pointsRecords,
    total,
    page,
    pageSize,
    isLoading,
    listMembers,
    getPointsRecords,
  } = useMemberStore();

  const [selectedMemberId, setSelectedMemberId] = useState<number | undefined>();
  const [modalType, setModalType] = useState<'add' | 'subtract' | null>(null);

  useEffect(() => {
    listMembers({ page_size: 100 });
  }, []);

  useEffect(() => {
    if (selectedMemberId) {
      getPointsRecords(selectedMemberId, 1, 10);
    }
  }, [selectedMemberId]);

  const handleRefresh = () => {
    listMembers({ page_size: 100 });
    if (selectedMemberId) {
      getPointsRecords(selectedMemberId, page, pageSize);
    }
  };

  /**
   * 处理会员选择变化
   */
  const handleMemberChange = (memberId: number | undefined) => {
    setSelectedMemberId(memberId);
  };

  /**
   * 处理分页变化
   */
  const handlePageChange = (newPage: number, newPageSize: number) => {
    if (selectedMemberId) {
      getPointsRecords(selectedMemberId, newPage, newPageSize);
    }
  };

  /**
   * 处理表单提交成功
   */
  const handleFormSuccess = () => {
    setModalType(null);
    if (selectedMemberId) {
      getPointsRecords(selectedMemberId, page, pageSize);
      listMembers({ page_size: 100 });
    }
  };

  const columns: ColumnsType<PointsRecord> = [
    {
      title: '记录ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type: string) => (
        <Tag color={type === 'add' ? 'green' : 'red'}>
          {getPointsTypeLabel(type)}
        </Tag>
      ),
    },
    {
      title: '积分',
      dataIndex: 'points',
      key: 'points',
      width: 100,
      render: (points: number, record) => (
        <span className={record.type === 'add' ? 'text-green-500' : 'text-red-500'}>
          {record.type === 'add' ? '+' : '-'}{points}
        </span>
      ),
    },
    {
      title: '原因',
      dataIndex: 'reason',
      key: 'reason',
      ellipsis: true,
    },
    {
      title: '时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm:ss'),
    },
  ];

  const selectedMember = members.find((m) => m.id === selectedMemberId);

  return (
    <div className="p-6">
      <Card
        title="积分记录"
        extra={
          <Button
            icon={<ReloadOutlined />}
            onClick={handleRefresh}
          >
            刷新
          </Button>
        }
      >
        <div className="mb-4">
          <Space size="middle" wrap>
            <Select
              placeholder="请选择会员"
              style={{ width: 250 }}
              showSearch
              optionFilterProp="label"
              value={selectedMemberId}
              onChange={handleMemberChange}
              options={members.map((m) => ({
                value: m.id,
                label: `${m.name} (${m.phone}) - 积分: ${m.points}`,
              }))}
            />
            {selectedMemberId && (
              <>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={() => setModalType('add')}
                >
                  增加积分
                </Button>
                <Button
                  icon={<MinusOutlined />}
                  onClick={() => setModalType('subtract')}
                >
                  减少积分
                </Button>
              </>
            )}
          </Space>
        </div>

        {selectedMember && (
          <div className="mb-4 p-4 bg-gray-50 rounded">
            <Space size="large">
              <span>会员：<strong>{selectedMember.name}</strong></span>
              <span>手机号：<strong>{selectedMember.phone}</strong></span>
              <span>当前积分：<strong className="text-orange-500">{selectedMember.points}</strong></span>
            </Space>
          </div>
        )}

        {!selectedMemberId && (
          <div className="text-center py-10 text-gray-400">
            请先选择会员查看积分记录
          </div>
        )}

        {selectedMemberId && (
          <>
            <Table
              columns={columns}
              dataSource={pointsRecords}
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
          </>
        )}
      </Card>

      <Modal
        title={modalType === 'add' ? '增加积分' : '减少积分'}
        open={modalType !== null}
        onCancel={() => setModalType(null)}
        footer={null}
        width={500}
        destroyOnHidden
      >
        {modalType && (
          <PointsForm
            type={modalType}
            onSuccess={handleFormSuccess}
            onCancel={() => setModalType(null)}
          />
        )}
      </Modal>
    </div>
  );
};

export default PointsRecordPage;
