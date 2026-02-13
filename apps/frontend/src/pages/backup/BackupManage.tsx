/**
 * 备份管理页面
 */
import React, { useEffect, useState } from 'react';
import {
  Button,
  Table,
  Modal,
  Form,
  Input,
  message,
  Popconfirm,
  Tag,
  Space,
  Card,
} from 'antd';
import {
  PlusOutlined,
  DownloadOutlined,
  ReloadOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import useBackupStore from '@/store/backupStore';
import type { Backup, BackupCreateParams } from '@/types/backup';

/**
 * 备份管理页面组件
 */
const BackupManage: React.FC = () => {
  const [isCreateModalVisible, setIsCreateModalVisible] = useState(false);
  const [isRestoreModalVisible, setIsRestoreModalVisible] = useState(false);
  const [selectedBackup, setSelectedBackup] = useState<Backup | null>(null);
  const [form] = Form.useForm();

  const {
    backups,
    isLoading,
    error,
    getBackups,
    createBackup,
    deleteBackup,
    downloadBackup,
    restoreBackup,
    clearError,
  } = useBackupStore();

  useEffect(() => {
    getBackups();
  }, [getBackups]);

  useEffect(() => {
    if (error) {
      message.error(error);
      clearError();
    }
  }, [error, clearError]);

  /**
   * 显示创建备份弹窗
   */
  const showCreateModal = () => {
    form.resetFields();
    setIsCreateModalVisible(true);
  };

  /**
   * 处理创建备份
   */
  const handleCreate = async () => {
    try {
      const values = await form.validateFields();
      const params: BackupCreateParams = {
        name: values.name,
        description: values.description,
      };

      await createBackup(params);
      message.success('备份创建成功');
      setIsCreateModalVisible(false);
    } catch (err) {
      console.error('创建备份失败:', err);
    }
  };

  /**
   * 处理删除备份
   */
  const handleDelete = async (id: number) => {
    try {
      await deleteBackup(id);
      message.success('备份删除成功');
    } catch (err) {
      console.error('删除备份失败:', err);
    }
  };

  /**
   * 处理下载备份
   */
  const handleDownload = async (backup: Backup) => {
    try {
      await downloadBackup(backup.id, backup.name);
      message.success('备份下载成功');
    } catch (err) {
      console.error('下载备份失败:', err);
    }
  };

  /**
   * 显示恢复确认弹窗
   */
  const showRestoreModal = (backup: Backup) => {
    setSelectedBackup(backup);
    setIsRestoreModalVisible(true);
  };

  /**
   * 处理恢复备份
   */
  const handleRestore = async () => {
    if (!selectedBackup) return;

    try {
      const result = await restoreBackup(selectedBackup.id);
      message.success(`数据恢复成功！恢复了 ${result.restored_counts.orders} 条订单、${result.restored_counts.transactions} 条收支记录`);
      setIsRestoreModalVisible(false);
      setSelectedBackup(null);
    } catch (err) {
      console.error('恢复备份失败:', err);
    }
  };

  /**
   * 格式化文件大小
   */
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  /**
   * 获取状态标签
   */
  const getStatusTag = (status: string) => {
    const statusMap: Record<string, { color: string; text: string }> = {
      pending: { color: 'default', text: '等待中' },
      in_progress: { color: 'processing', text: '进行中' },
      completed: { color: 'success', text: '已完成' },
      failed: { color: 'error', text: '失败' },
    };
    const config = statusMap[status] || { color: 'default', text: status };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  /**
   * 获取备份类型标签
   */
  const getTypeTag = (type: string) => {
    return type === 'auto' ? (
      <Tag color="blue">自动</Tag>
    ) : (
      <Tag color="green">手动</Tag>
    );
  };

  const columns: ColumnsType<Backup> = [
    {
      title: '备份名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      width: 200,
      ellipsis: true,
    },
    {
      title: '类型',
      dataIndex: 'backup_type',
      key: 'backup_type',
      width: 80,
      render: (type: string) => getTypeTag(type),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => getStatusTag(status),
    },
    {
      title: '大小',
      dataIndex: 'backup_size',
      key: 'backup_size',
      width: 100,
      render: (size: number) => formatFileSize(size),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm:ss'),
    },
    {
      title: '完成时间',
      dataIndex: 'completed_at',
      key: 'completed_at',
      width: 180,
      render: (date: string | null) =>
        date ? dayjs(date).format('YYYY-MM-DD HH:mm:ss') : '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_: unknown, record: Backup) => (
        <Space size="small">
          <Button
            type="link"
            size="small"
            icon={<DownloadOutlined />}
            onClick={() => handleDownload(record)}
            disabled={record.status !== 'completed'}
          >
            下载
          </Button>
          <Button
            type="link"
            size="small"
            icon={<ReloadOutlined />}
            onClick={() => showRestoreModal(record)}
            disabled={record.status !== 'completed'}
          >
            恢复
          </Button>
          <Popconfirm
            title="确定要删除这个备份吗？"
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
        title="备份管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={showCreateModal}>
            创建备份
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={backups.map((backup) => ({ ...backup, key: backup.id }))}
          loading={isLoading}
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 创建备份弹窗 */}
      <Modal
        title="创建备份"
        open={isCreateModalVisible}
        onOk={handleCreate}
        onCancel={() => setIsCreateModalVisible(false)}
        confirmLoading={isLoading}
        okText="创建"
        cancelText="取消"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="备份名称"
            rules={[{ required: true, message: '请输入备份名称' }]}
          >
            <Input placeholder="请输入备份名称" maxLength={64} />
          </Form.Item>
          <Form.Item name="description" label="备份描述">
            <Input.TextArea
              placeholder="请输入备份描述（可选）"
              rows={3}
              maxLength={500}
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 恢复确认弹窗 */}
      <Modal
        title="恢复备份"
        open={isRestoreModalVisible}
        onOk={handleRestore}
        onCancel={() => {
          setIsRestoreModalVisible(false);
          setSelectedBackup(null);
        }}
        confirmLoading={isLoading}
        okText="确认恢复"
        cancelText="取消"
        okButtonProps={{ danger: true }}
      >
        <div className="py-4">
          <p className="text-red-500 font-medium mb-4">
            ⚠️ 警告：恢复操作将会覆盖当前所有数据！
          </p>
          <p className="text-gray-600 mb-2">
            备份名称：{selectedBackup?.name}
          </p>
          <p className="text-gray-600 mb-2">
            备份时间：{selectedBackup?.created_at
              ? dayjs(selectedBackup.created_at).format('YYYY-MM-DD HH:mm:ss')
              : '-'}
          </p>
          <p className="text-gray-500 mt-4">
            恢复过程中请不要关闭页面，恢复完成后请刷新页面查看数据。
          </p>
        </div>
      </Modal>
    </div>
  );
};

export default BackupManage;
