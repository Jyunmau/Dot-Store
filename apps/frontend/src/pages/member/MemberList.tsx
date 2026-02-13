/**
 * 会员列表页面
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
  Pagination,
  Form,
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
import { useMemberStore } from '@/store/memberStore';
import type { Member, MemberCreateParams, MemberUpdateParams } from '@/types/member';
import { getMemberLevelLabel, MEMBER_LEVEL_OPTIONS } from '@/types/member';

/**
 * 会员表单组件
 */
interface MemberFormProps {
  member?: Member | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const MemberForm: React.FC<MemberFormProps> = ({ member, onSuccess, onCancel }) => {
  const [form] = Form.useForm();
  const { createMember, updateMember } = useMemberStore();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (member) {
      form.setFieldsValue({
        name: member.name,
        phone: member.phone,
        level: member.level,
      });
    } else {
      form.resetFields();
    }
  }, [member, form]);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      if (member) {
        await updateMember(member.id, values as MemberUpdateParams);
        message.success('会员更新成功');
      } else {
        await createMember(values as MemberCreateParams);
        message.success('会员创建成功');
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
        name="name"
        label="会员姓名"
        rules={[{ required: true, message: '请输入会员姓名' }]}
      >
        <Input placeholder="请输入会员姓名" maxLength={64} />
      </Form.Item>
      <Form.Item
        name="phone"
        label="手机号"
        rules={[{ required: true, message: '请输入手机号' }]}
      >
        <Input placeholder="请输入手机号" maxLength={32} />
      </Form.Item>
      <Form.Item
        name="level"
        label="会员等级"
        initialValue="normal"
        rules={[{ required: true, message: '请选择会员等级' }]}
      >
        <Select placeholder="请选择会员等级" options={MEMBER_LEVEL_OPTIONS} />
      </Form.Item>
      <Form.Item className="mb-0 flex justify-end">
        <Space>
          <Button onClick={onCancel}>取消</Button>
          <Button type="primary" htmlType="submit" loading={loading}>
            {member ? '更新' : '创建'}
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

/**
 * 会员列表页面组件
 */
const MemberListPage: React.FC = () => {
  const {
    members,
    total,
    page,
    pageSize,
    isLoading,
    listMembers,
    deleteMember,
  } = useMemberStore();

  const [filters, setFilters] = useState<{
    level?: string;
    keyword?: string;
    page?: number;
    page_size?: number;
  }>({});

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingMember, setEditingMember] = useState<Member | null>(null);

  useEffect(() => {
    listMembers(filters);
  }, [filters]);

  /**
   * 处理删除会员
   */
  const handleDelete = async (memberId: number) => {
    try {
      await deleteMember(memberId);
      message.success('会员删除成功');
    } catch {
      message.error('会员删除失败');
    }
  };

  /**
   * 处理编辑会员
   */
  const handleEdit = (member: Member) => {
    setEditingMember(member);
    setIsModalOpen(true);
  };

  /**
   * 处理新增会员
   */
  const handleAdd = () => {
    setEditingMember(null);
    setIsModalOpen(true);
  };

  /**
   * 处理表单提交成功
   */
  const handleFormSuccess = () => {
    setIsModalOpen(false);
    setEditingMember(null);
    listMembers(filters);
  };

  /**
   * 处理筛选条件变化
   */
  const handleFilterChange = (key: string, value: string | undefined) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
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

  const columns: ColumnsType<Member> = [
    {
      title: '会员ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name',
      width: 120,
    },
    {
      title: '手机号',
      dataIndex: 'phone',
      key: 'phone',
      width: 150,
    },
    {
      title: '会员等级',
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (level: string) => (
        <Tag color={level === 'vip' ? 'gold' : 'blue'}>
          {getMemberLevelLabel(level)}
        </Tag>
      ),
    },
    {
      title: '积分',
      dataIndex: 'points',
      key: 'points',
      width: 100,
      render: (points: number) => (
        <span className="text-orange-500 font-medium">{points}</span>
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
            title="确定要删除此会员吗？"
            description="删除后无法恢复"
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
      <Card
        title="会员管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新增会员
          </Button>
        }
      >
        <div className="mb-4">
          <Space size="middle" wrap>
            <Select
              placeholder="会员等级"
              allowClear
              style={{ width: 120 }}
              value={filters.level}
              onChange={(value) => handleFilterChange('level', value)}
              options={MEMBER_LEVEL_OPTIONS}
            />
            <Input
              placeholder="搜索姓名或手机号"
              prefix={<SearchOutlined />}
              style={{ width: 200 }}
              value={filters.keyword}
              onChange={(e) => handleFilterChange('keyword', e.target.value || undefined)}
              allowClear
            />
            <Button icon={<ReloadOutlined />} onClick={handleReset}>
              重置
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={members}
          rowKey="id"
          loading={isLoading}
          pagination={false}
          scroll={{ x: 900 }}
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
        title={editingMember ? '编辑会员' : '新增会员'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingMember(null);
        }}
        footer={null}
        width={500}
        destroyOnHidden
      >
        <MemberForm
          member={editingMember}
          onSuccess={handleFormSuccess}
          onCancel={() => {
            setIsModalOpen(false);
            setEditingMember(null);
          }}
        />
      </Modal>
    </div>
  );
};

export default MemberListPage;
