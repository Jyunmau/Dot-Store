/**
 * 店员管理页面
 */
import React, { useEffect, useState } from 'react';
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  Checkbox,
  message,
  Space,
  Card,
  Popconfirm,
  Tag,
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
  UserOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { authService, permissionService } from '@/services';
import type { Staff, PermissionGroups } from '@/types/user';

const { Option } = Select;

const StaffManagementPage: React.FC = () => {
  const [staffList, setStaffList] = useState<Staff[]>([]);
  const [permissionGroups, setPermissionGroups] = useState<PermissionGroups>({});
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [permissionModalVisible, setPermissionModalVisible] = useState(false);
  const [currentStaff, setCurrentStaff] = useState<Staff | null>(null);
  const [form] = Form.useForm();
  const [permissionForm] = Form.useForm();

  useEffect(() => {
    loadStaffList();
    loadPermissionGroups();
  }, []);

  /**
   * 加载店员列表
   */
  const loadStaffList = async () => {
    setLoading(true);
    try {
      const data = await authService.getStaffList();
      setStaffList(data);
    } catch {
      message.error('加载店员列表失败');
    } finally {
      setLoading(false);
    }
  };

  /**
   * 加载权限分组
   */
  const loadPermissionGroups = async () => {
    try {
      const data = await permissionService.getPermissionGroups();
      setPermissionGroups(data);
    } catch {
      message.error('加载权限分组失败');
    }
  };

  /**
   * 打开添加店员弹窗
   */
  const handleAddStaff = () => {
    setCurrentStaff(null);
    form.resetFields();
    setModalVisible(true);
  };

  /**
   * 打开编辑权限弹窗
   */
  const handleEditPermissions = (staff: Staff) => {
    setCurrentStaff(staff);
    permissionForm.setFieldsValue({
      permissions: staff.permissions || [],
    });
    setPermissionModalVisible(true);
  };

  /**
   * 提交添加店员
   */
  const handleSubmitStaff = async (values: {
    phone?: string;
    email?: string;
    password: string;
  }) => {
    try {
      await authService.createStaff(values);
      message.success('添加店员成功');
      setModalVisible(false);
      loadStaffList();
    } catch {
      message.error('添加店员失败');
    }
  };

  /**
   * 提交更新权限
   */
  const handleSubmitPermissions = async (values: { permissions: string[] }) => {
    if (!currentStaff) return;
    try {
      await authService.updateStaffPermissions(currentStaff.id, values);
      message.success('更新权限成功');
      setPermissionModalVisible(false);
      loadStaffList();
    } catch {
      message.error('更新权限失败');
    }
  };

  /**
   * 删除店员
   */
  const handleDeleteStaff = async (staffId: number) => {
    try {
      await authService.removeStaff(staffId);
      message.success('移除店员成功');
      loadStaffList();
    } catch {
      message.error('移除店员失败');
    }
  };

  const columns: ColumnsType<Staff> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '手机号',
      dataIndex: 'phone',
      key: 'phone',
      render: (phone: string) => phone || '-',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
      render: (email: string) => email || '-',
    },
    {
      title: '店铺名称',
      dataIndex: 'shop_name',
      key: 'shop_name',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '正常' : '禁用'}
        </Tag>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEditPermissions(record)}
          >
            权限
          </Button>
          <Popconfirm
            title="确定要移除该店员吗？"
            onConfirm={() => handleDeleteStaff(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              移除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="p-6">
      <Card
        title={
          <div className="flex items-center">
            <UserOutlined className="mr-2" />
            <span>店员管理</span>
          </div>
        }
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAddStaff}>
            添加店员
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={staffList}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
          }}
        />
      </Card>

      {/* 添加店员弹窗 */}
      <Modal
        title="添加店员"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmitStaff}>
          <Form.Item
            name="phone"
            label="手机号"
            rules={[
              { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' },
            ]}
          >
            <Input placeholder="请输入手机号（可选）" />
          </Form.Item>

          <Form.Item
            name="email"
            label="邮箱"
            rules={[{ type: 'email', message: '邮箱格式不正确' }]}
          >
            <Input placeholder="请输入邮箱（可选）" />
          </Form.Item>

          <Form.Item
            name="password"
            label="密码"
            rules={[
              { required: true, message: '请输入密码' },
              { min: 8, message: '密码至少8位' },
              { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/, message: '密码需包含字母和数字' },
            ]}
          >
            <Input.Password placeholder="请输入密码" />
          </Form.Item>

          <Form.Item>
            <Space className="w-full justify-end">
              <Button onClick={() => setModalVisible(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                确定
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 编辑权限弹窗 */}
      <Modal
        title="编辑权限"
        open={permissionModalVisible}
        onCancel={() => setPermissionModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form form={permissionForm} layout="vertical" onFinish={handleSubmitPermissions}>
          {Object.entries(permissionGroups).map(([key, group]) => (
            <Form.Item key={key} label={group.name}>
              <Checkbox.Group
                className="flex flex-wrap gap-4"
              >
                {group.permissions.map((perm) => (
                  <Checkbox key={perm.key} value={perm.key}>
                    {perm.name}
                  </Checkbox>
                ))}
              </Checkbox.Group>
            </Form.Item>
          ))}

          <Form.Item name="permissions" hidden>
            <Input />
          </Form.Item>

          <Form.Item>
            <Space className="w-full justify-end">
              <Button onClick={() => setPermissionModalVisible(false)}>取消</Button>
              <Button type="primary" htmlType="submit">
                确定
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default StaffManagementPage;
