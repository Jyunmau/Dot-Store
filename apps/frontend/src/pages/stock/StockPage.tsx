/**
 * 库存管理页面
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
  Input,
  Form,
  InputNumber,
  Tag,
  Select,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SearchOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import { useStockStore } from '@/store/stockStore';
import type { Ingredient, IngredientCreateParams, IngredientUpdateParams } from '@/types/stock';

/**
 * 食材管理页面组件
 */
const IngredientListPage: React.FC = () => {
  const {
    ingredients,
    stockWarnings,
    total,
    isLoading,
    listIngredients,
    createIngredient,
    updateIngredient,
    deleteIngredient,
    getStockWarnings,
  } = useStockStore();

  const [searchName, setSearchName] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingIngredient, setEditingIngredient] = useState<Ingredient | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    listIngredients();
    getStockWarnings();
  }, [listIngredients, getStockWarnings]);

  /**
   * 处理搜索
   */
  const handleSearch = () => {
    listIngredients(searchName);
  };

  /**
   * 处理删除食材
   */
  const handleDelete = async (ingredientId: number) => {
    try {
      await deleteIngredient(ingredientId);
      message.success('食材删除成功');
      getStockWarnings();
    } catch {
      message.error('食材删除失败');
    }
  };

  /**
   * 处理编辑食材
   */
  const handleEdit = (ingredient: Ingredient) => {
    setEditingIngredient(ingredient);
    form.setFieldsValue({
      name: ingredient.name,
      unit: ingredient.unit,
      current_stock: Number(ingredient.current_stock),
      warning_stock: Number(ingredient.warning_stock),
    });
    setIsModalOpen(true);
  };

  /**
   * 处理新增食材
   */
  const handleAdd = () => {
    setEditingIngredient(null);
    form.resetFields();
    setIsModalOpen(true);
  };

  /**
   * 处理表单提交
   */
  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const params: IngredientCreateParams | IngredientUpdateParams = {
        name: values.name,
        unit: values.unit,
        current_stock: values.current_stock || 0,
        warning_stock: values.warning_stock || 0,
      };

      if (editingIngredient) {
        await updateIngredient(editingIngredient.id, params);
        message.success('食材更新成功');
      } else {
        await createIngredient(params as IngredientCreateParams);
        message.success('食材创建成功');
      }

      setIsModalOpen(false);
      setEditingIngredient(null);
      form.resetFields();
      listIngredients(searchName);
      getStockWarnings();
    } catch (error) {
      console.error('表单提交失败:', error);
    }
  };

  /**
   * 检查是否库存预警
   */
  const isLowStock = (ingredient: Ingredient) => {
    return Number(ingredient.current_stock) < Number(ingredient.warning_stock);
  };

  const columns: ColumnsType<Ingredient> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '食材名称',
      dataIndex: 'name',
      key: 'name',
      width: 150,
    },
    {
      title: '单位',
      dataIndex: 'unit',
      key: 'unit',
      width: 80,
    },
    {
      title: '当前库存',
      dataIndex: 'current_stock',
      key: 'current_stock',
      width: 120,
      render: (stock: string, record) => {
        const isLow = isLowStock(record);
        return (
          <span className={isLow ? 'text-red-500 font-medium' : ''}>
            {Number(stock).toFixed(2)}
            {isLow && <WarningOutlined className="ml-1 text-red-500" />}
          </span>
        );
      },
    },
    {
      title: '预警值',
      dataIndex: 'warning_stock',
      key: 'warning_stock',
      width: 100,
      render: (stock: string) => Number(stock).toFixed(2),
    },
    {
      title: '状态',
      key: 'status',
      width: 100,
      render: (_, record) => {
        const isLow = isLowStock(record);
        return isLow ? (
          <Tag color="error">库存不足</Tag>
        ) : (
          <Tag color="success">正常</Tag>
        );
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm'),
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
            title="确定要删除此食材吗？"
            description="删除后相关库存记录也会被删除"
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
        title={stockWarnings.length > 0 ? `食材管理 (${stockWarnings.length}个预警)` : '食材管理'}
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加食材
          </Button>
        }
      >
        <div className="mb-4">
          <Space>
            <Input
              placeholder="搜索食材名称"
              prefix={<SearchOutlined />}
              value={searchName}
              onChange={(e) => setSearchName(e.target.value)}
              onPressEnter={handleSearch}
              style={{ width: 200 }}
            />
            <Button type="primary" onClick={handleSearch}>
              搜索
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={ingredients}
          rowKey="id"
          loading={isLoading}
          pagination={{
            total,
            pageSize: 100,
            showTotal: (total) => `共 ${total} 条`,
          }}
          scroll={{ x: 1000 }}
        />
      </Card>

      <Modal
        title={editingIngredient ? '编辑食材' : '添加食材'}
        open={isModalOpen}
        onOk={handleSubmit}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingIngredient(null);
          form.resetFields();
        }}
        okText="保存"
        cancelText="取消"
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="食材名称"
            rules={[{ required: true, message: '请输入食材名称' }]}
          >
            <Input placeholder="请输入食材名称" maxLength={64} />
          </Form.Item>
          <Form.Item
            name="unit"
            label="单位"
            rules={[{ required: true, message: '请输入单位' }]}
          >
            <Input placeholder="如：千克、升、个" maxLength={16} />
          </Form.Item>
          <Form.Item
            name="current_stock"
            label="当前库存"
            initialValue={0}
          >
            <InputNumber
              placeholder="请输入当前库存"
              min={0}
              precision={2}
              style={{ width: '100%' }}
            />
          </Form.Item>
          <Form.Item
            name="warning_stock"
            label="预警值"
            initialValue={0}
          >
            <InputNumber
              placeholder="库存低于此值时预警"
              min={0}
              precision={2}
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

/**
 * 库存记录页面组件
 */
const StockRecordPage: React.FC = () => {
  const {
    ingredients,
    stockRecords,
    recordsTotal,
    recordsPage,
    isLoading,
    listIngredients,
    listStockRecords,
    recordStockIn,
    recordStockOut,
  } = useStockStore();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [recordType, setRecordType] = useState<'in' | 'out'>('in');
  const [form] = Form.useForm();

  useEffect(() => {
    listIngredients();
    listStockRecords();
  }, [listIngredients, listStockRecords]);

  /**
   * 打开入库弹窗
   */
  const handleStockIn = () => {
    setRecordType('in');
    form.resetFields();
    setIsModalOpen(true);
  };

  /**
   * 打开出库弹窗
   */
  const handleStockOut = () => {
    setRecordType('out');
    form.resetFields();
    setIsModalOpen(true);
  };

  /**
   * 处理表单提交
   */
  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const params = {
        ingredient_id: values.ingredient_id,
        quantity: values.quantity,
        note: values.note,
      };

      if (recordType === 'in') {
        await recordStockIn(params);
        message.success('入库记录成功');
      } else {
        await recordStockOut(params);
        message.success('出库记录成功');
      }

      setIsModalOpen(false);
      form.resetFields();
      listStockRecords();
    } catch (error) {
      console.error('记录失败:', error);
    }
  };

  const columns: ColumnsType<typeof stockRecords[0]> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '食材名称',
      dataIndex: 'ingredient_name',
      key: 'ingredient_name',
      width: 150,
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      width: 80,
      render: (type: string) => (
        <Tag color={type === 'in' ? 'green' : 'orange'}>
          {type === 'in' ? '入库' : '出库'}
        </Tag>
      ),
    },
    {
      title: '数量',
      dataIndex: 'quantity',
      key: 'quantity',
      width: 100,
      render: (quantity: string) => Number(quantity).toFixed(2),
    },
    {
      title: '单位',
      dataIndex: 'ingredient_unit',
      key: 'ingredient_unit',
      width: 80,
    },
    {
      title: '备注',
      dataIndex: 'note',
      key: 'note',
      width: 200,
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

  return (
    <div className="p-6">
      <Card
        title="库存记录"
        extra={
          <Space>
            <Button type="primary" onClick={handleStockIn}>
              入库
            </Button>
            <Button onClick={handleStockOut}>出库</Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={stockRecords}
          rowKey="id"
          loading={isLoading}
          pagination={{
            current: recordsPage,
            total: recordsTotal,
            pageSize: 20,
            showTotal: (total) => `共 ${total} 条`,
          }}
          scroll={{ x: 900 }}
        />
      </Card>

      <Modal
        title={recordType === 'in' ? '入库记录' : '出库记录'}
        open={isModalOpen}
        onOk={handleSubmit}
        onCancel={() => {
          setIsModalOpen(false);
          form.resetFields();
        }}
        okText="保存"
        cancelText="取消"
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="ingredient_id"
            label="食材"
            rules={[{ required: true, message: '请选择食材' }]}
          >
            <Select
              placeholder="请选择食材"
              showSearch
              optionFilterProp="label"
              options={ingredients.map((ing) => ({
                value: ing.id,
                label: `${ing.name} (库存: ${Number(ing.current_stock).toFixed(2)} ${ing.unit})`,
              }))}
            />
          </Form.Item>
          <Form.Item
            name="quantity"
            label="数量"
            rules={[{ required: true, message: '请输入数量' }]}
          >
            <InputNumber
              placeholder="请输入数量"
              min={0.01}
              precision={2}
              style={{ width: '100%' }}
            />
          </Form.Item>
          <Form.Item name="note" label="备注">
            <Input.TextArea placeholder="请输入备注" rows={3} maxLength={500} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

/**
 * 库存预警页面组件
 */
const StockWarningPage: React.FC = () => {
  const { stockWarnings, isLoading, getStockWarnings } = useStockStore();

  useEffect(() => {
    getStockWarnings();
  }, [getStockWarnings]);

  const columns: ColumnsType<typeof stockWarnings[0]> = [
    {
      title: '食材ID',
      dataIndex: 'ingredient_id',
      key: 'ingredient_id',
      width: 80,
    },
    {
      title: '食材名称',
      dataIndex: 'name',
      key: 'name',
      width: 150,
    },
    {
      title: '单位',
      dataIndex: 'unit',
      key: 'unit',
      width: 80,
    },
    {
      title: '当前库存',
      dataIndex: 'current_stock',
      key: 'current_stock',
      width: 120,
      render: (stock: string) => (
        <span className="text-red-500 font-medium">{Number(stock).toFixed(2)}</span>
      ),
    },
    {
      title: '预警值',
      dataIndex: 'warning_stock',
      key: 'warning_stock',
      width: 100,
      render: (stock: string) => Number(stock).toFixed(2),
    },
    {
      title: '缺口',
      dataIndex: 'deficit',
      key: 'deficit',
      width: 100,
      render: (deficit: string) => (
        <span className="text-orange-500 font-medium">{Number(deficit).toFixed(2)}</span>
      ),
    },
  ];

  return (
    <div className="p-6">
      <Card
        title="库存预警"
        extra={
          <Button onClick={() => getStockWarnings()}>刷新</Button>
        }
      >
        {stockWarnings.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>暂无库存预警</p>
          </div>
        ) : (
          <Table
            columns={columns}
            dataSource={stockWarnings}
            rowKey="ingredient_id"
            loading={isLoading}
            pagination={false}
          />
        )}
      </Card>
    </div>
  );
};

export { IngredientListPage, StockRecordPage, StockWarningPage };
export default IngredientListPage;
