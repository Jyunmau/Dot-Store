/**
 * 收支分类管理页面
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
  Form,
  Input,
  Select,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useTransactionStore } from '@/store/transactionStore';
import type { TransactionCategory, TransactionCategoryCreateParams, TransactionCategoryUpdateParams } from '@/types/transaction';
import { getTransactionTypeLabel, getTransactionTypeColor } from '@/types/transaction';

/**
 * 收支分类管理页面组件
 */
const TransactionCategoryManagePage: React.FC = () => {
  const {
    categories,
    isLoading,
    listCategories,
    createCategory,
    updateCategory,
    deleteCategory,
  } = useTransactionStore();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<TransactionCategory | null>(null);
  const [form] = Form.useForm();
  const [filterType, setFilterType] = useState<'income' | 'expense' | undefined>(undefined);

  useEffect(() => {
    listCategories(filterType);
  }, [listCategories, filterType]);

  /**
   * 处理删除分类
   */
  const handleDelete = async (categoryId: number) => {
    try {
      await deleteCategory(categoryId);
      message.success('分类删除成功');
    } catch {
      message.error('分类删除失败');
    }
  };

  /**
   * 处理编辑分类
   */
  const handleEdit = (category: TransactionCategory) => {
    setEditingCategory(category);
    form.setFieldsValue({
      name: category.name,
      type: category.type,
      description: category.description,
    });
    setIsModalOpen(true);
  };

  /**
   * 处理新增分类
   */
  const handleAdd = () => {
    setEditingCategory(null);
    form.resetFields();
    setIsModalOpen(true);
  };

  /**
   * 处理表单提交
   */
  const handleSubmit = async (values: TransactionCategoryCreateParams | TransactionCategoryUpdateParams) => {
    try {
      if (editingCategory) {
        await updateCategory(editingCategory.id, values as TransactionCategoryUpdateParams);
        message.success('更新成功');
      } else {
        await createCategory(values as TransactionCategoryCreateParams);
        message.success('创建成功');
      }
      setIsModalOpen(false);
      form.resetFields();
      listCategories(filterType);
    } catch {
      message.error(editingCategory ? '更新失败' : '创建失败');
    }
  };

  const columns: ColumnsType<TransactionCategory> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '分类名称',
      dataIndex: 'name',
      key: 'name',
      width: 150,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      width: 100,
      render: (type: string) => (
        <Tag color={getTransactionTypeColor(type)}>{getTransactionTypeLabel(type)}</Tag>
      ),
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (description: string | null) => description || '-',
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
            title="确定要删除此分类吗？"
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
        title="收支分类管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新增分类
          </Button>
        }
      >
        <div className="mb-4">
          <Space>
            <span>类型筛选：</span>
            <Select
              placeholder="全部类型"
              allowClear
              style={{ width: 120 }}
              value={filterType}
              onChange={(value) => setFilterType(value)}
              options={[
                { value: 'income', label: '收入' },
                { value: 'expense', label: '支出' },
              ]}
            />
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={categories}
          rowKey="id"
          loading={isLoading}
          pagination={false}
        />
      </Card>

      <Modal
        title={editingCategory ? '编辑分类' : '新增分类'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          form.resetFields();
        }}
        footer={null}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            type: 'income',
          }}
        >
          <Form.Item
            name="name"
            label="分类名称"
            rules={[{ required: true, message: '请输入分类名称' }]}
          >
            <Input placeholder="请输入分类名称" />
          </Form.Item>

          <Form.Item
            name="type"
            label="类型"
            rules={[{ required: true, message: '请选择类型' }]}
          >
            <Select placeholder="请选择类型" disabled={!!editingCategory}>
              <Select.Option value="income">收入</Select.Option>
              <Select.Option value="expense">支出</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item name="description" label="描述">
            <Input.TextArea rows={3} placeholder="请输入描述" />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingCategory ? '更新' : '创建'}
              </Button>
              <Button onClick={() => setIsModalOpen(false)}>取消</Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default TransactionCategoryManagePage;
