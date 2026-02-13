/**
 * 订单表单组件
 */
import React, { useEffect } from 'react';
import { Form, Input, InputNumber, Select, Button, Space, message } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import { useOrderStore } from '@/store/orderStore';
import type { Order, OrderCreateParams, OrderUpdateParams } from '@/types/order';
import { ORDER_TYPE_OPTIONS, ORDER_STATUS_OPTIONS } from '@/types/order';

interface OrderFormProps {
  order?: Order | null;
  onSuccess: () => void;
  onCancel: () => void;
}

/**
 * 订单表单组件
 */
const OrderForm: React.FC<OrderFormProps> = ({ order, onSuccess, onCancel }) => {
  const [form] = Form.useForm();
  const { createOrder, updateOrder, isLoading, categories, listCategories } = useOrderStore();

  useEffect(() => {
    listCategories();
    if (order) {
      form.setFieldsValue({
        amount: parseFloat(order.amount),
        order_type: order.order_type,
        category_id: order.category_id,
        tags: order.tags || [],
        status: order.status,
      });
    } else {
      form.resetFields();
    }
  }, [order, form, listCategories]);

  /**
   * 处理表单提交
   */
  const handleSubmit = async (values: OrderCreateParams | OrderUpdateParams) => {
    try {
      if (order) {
        await updateOrder(order.id, values);
        message.success('订单更新成功');
      } else {
        await createOrder(values as OrderCreateParams);
        message.success('订单创建成功');
      }
      form.resetFields();
      onSuccess();
    } catch {
      message.error(order ? '订单更新失败' : '订单创建失败');
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      preserve={false}
      initialValues={{
        order_type: 'dine_in',
        status: 'recorded',
        tags: [],
      }}
    >
      <Form.Item
        name="amount"
        label="金额"
        rules={[
          { required: true, message: '请输入金额' },
          { type: 'number', min: 0.01, message: '金额必须大于0' },
        ]}
      >
        <InputNumber
          prefix="¥"
          precision={2}
          min={0.01}
          style={{ width: '100%' }}
          placeholder="请输入订单金额"
        />
      </Form.Item>

      <Form.Item
        name="order_type"
        label="订单类型"
        rules={[{ required: true, message: '请选择订单类型' }]}
      >
        <Select placeholder="请选择订单类型" options={ORDER_TYPE_OPTIONS} />
      </Form.Item>

      <Form.Item name="category_id" label="分类">
        <Select
          placeholder="请选择分类"
          allowClear
          options={categories.map((c) => ({ value: c.id, label: c.name }))}
        />
      </Form.Item>

      <Form.Item label="标签">
        <Form.List name="tags">
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ key, name, ...restField }) => (
                <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                  <Form.Item
                    {...restField}
                    name={name}
                    rules={[{ required: false }]}
                  >
                    <Input placeholder="请输入标签" style={{ width: 200 }} />
                  </Form.Item>
                  <MinusCircleOutlined onClick={() => remove(name)} />
                </Space>
              ))}
              <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                添加标签
              </Button>
            </>
          )}
        </Form.List>
      </Form.Item>

      {order && (
        <Form.Item name="status" label="状态">
          <Select placeholder="请选择状态" options={ORDER_STATUS_OPTIONS} />
        </Form.Item>
      )}

      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={isLoading}>
            {order ? '更新' : '创建'}
          </Button>
          <Button onClick={onCancel}>取消</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default OrderForm;
