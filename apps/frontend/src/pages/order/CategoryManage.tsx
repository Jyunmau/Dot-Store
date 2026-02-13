/**
 * 订单分类管理页面
 */
import React, { useEffect, useState } from 'react';
import {
  Table,
  Button,
  Space,
  Modal,
  message,
  Popconfirm,
  Card,
  Form,
  Input,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useOrderStore } from '@/store/orderStore';
import type { OrderCategory, OrderCategoryCreateParams, OrderCategoryUpdateParams } from '@/types/order';

/**
 * 订单分类管理页面组件
 */
const CategoryManagePage: React.FC = () => {
  const {
    categories,
    isLoading,
    listCategories,
    createCategory,
    updateCategory,
    deleteCategory,
  } = useOrderStore();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<OrderCategory | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    listCategories();
  }, [listCategories]);

  /**
   * 处理删除分类
   */
  const handleDelete = async (categoryId: number) => {
    try {
      await deleteCategory(categoryId);
      message.success('分类删除成功');
    } catch {
      message.error('分类删除失败，可能该分类下有订单');
    }
  };

  /**
   * 处理编辑分类
   */
  const handleEdit = (category: OrderCategory) => {
    setEditingCategory(category);
    form.setFieldsValue({
      name: category.name,
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
  const handleSubmit = async (values: OrderCategoryCreateParams | OrderCategoryUpdateParams) => {
    try {
      if (editingCategory) {
        await updateCategory(editingCategory.id, values);
        message.success('分类更新成功');
      } else {
        await createCategory(values as OrderCategoryCreateParams);
        message.success('分类创建成功');
      }
      setIsModalOpen(false);
      form.resetFields();
      setEditingCategory(null);
    } catch {
      message.error(editingCategory ? '分类更新失败' : '分类创建失败');
    }
  };

  const columns: ColumnsType<OrderCategory> = [
    {
      title: '分类ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '分类名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
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
            title="确定要删除此分类吗？"
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
        title="订单分类管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新增分类
          </Button>
        }
      >
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
          setEditingCategory(null);
          form.resetFields();
        }}
        footer={null}
        destroyOnHidden
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          preserve={false}
        >
          <Form.Item
            name="name"
            label="分类名称"
            rules={[
              { required: true, message: '请输入分类名称' },
              { max: 64, message: '分类名称不能超过64个字符' },
            ]}
          >
            <Input placeholder="请输入分类名称" maxLength={64} />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ max: 256, message: '描述不能超过256个字符' }]}
          >
            <Input.TextArea
              placeholder="请输入分类描述"
              rows={3}
              maxLength={256}
              showCount
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={isLoading}>
                {editingCategory ? '更新' : '创建'}
              </Button>
              <Button
                onClick={() => {
                  setIsModalOpen(false);
                  setEditingCategory(null);
                  form.resetFields();
                }}
              >
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CategoryManagePage;
