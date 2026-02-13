/**
 * 收支记录表单组件
 */
import React, { useEffect, useState } from 'react';
import { Form, Input, InputNumber, Select, Button, Space, Upload, message } from 'antd';
import { PlusOutlined, LoadingOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import type { Transaction, TransactionCreateParams, TransactionUpdateParams } from '@/types/transaction';
import { useTransactionStore } from '@/store/transactionStore';
import { transactionService } from '@/services/transactionService';

interface TransactionFormProps {
  transaction?: Transaction | null;
  onSuccess: () => void;
  onCancel: () => void;
}

/**
 * 收支记录表单组件
 */
const TransactionForm: React.FC<TransactionFormProps> = ({ transaction, onSuccess, onCancel }) => {
  const [form] = Form.useForm();
  const { createTransaction, updateTransaction, listCategories, categories } = useTransactionStore();
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [attachmentUrl, setAttachmentUrl] = useState<string | null>(transaction?.attachment_url || null);

  useEffect(() => {
    listCategories();
    if (transaction) {
      form.setFieldsValue({
        type: transaction.type,
        category: transaction.category,
        amount: parseFloat(transaction.amount),
        note: transaction.note,
      });
      setAttachmentUrl(transaction.attachment_url);
    }
  }, [transaction, form, listCategories]);

  /**
   * 处理文件上传
   */
  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      const response = await transactionService.uploadAttachment(file);
      setAttachmentUrl(response.url);
      message.success('上传成功');
    } catch {
      message.error('上传失败');
    } finally {
      setUploading(false);
    }
  };

  const uploadProps: UploadProps = {
    beforeUpload: (file) => {
      const isImage = file.type.startsWith('image/');
      if (!isImage) {
        message.error('只能上传图片文件！');
        return false;
      }
      const isLt5M = file.size / 1024 / 1024 < 5;
      if (!isLt5M) {
        message.error('图片大小不能超过 5MB！');
        return false;
      }
      handleUpload(file);
      return false;
    },
    showUploadList: false,
  };

  /**
   * 处理表单提交
   */
  const handleSubmit = async (values: TransactionCreateParams | TransactionUpdateParams) => {
    setLoading(true);
    try {
      const data = {
        ...values,
        amount: Number(values.amount),
        attachment_url: attachmentUrl,
      };

      if (transaction) {
        await updateTransaction(transaction.id, data as TransactionUpdateParams);
        message.success('更新成功');
      } else {
        await createTransaction(data as TransactionCreateParams);
        message.success('创建成功');
      }
      onSuccess();
    } catch {
      message.error(transaction ? '更新失败' : '创建失败');
    } finally {
      setLoading(false);
    }
  };

  const selectedType = Form.useWatch('type', form);
  const filteredCategories = categories.filter((c) => c.type === selectedType);

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      preserve={false}
      initialValues={{
        type: 'income',
      }}
    >
      <Form.Item
        name="type"
        label="类型"
        rules={[{ required: true, message: '请选择类型' }]}
      >
        <Select placeholder="请选择类型">
          <Select.Option value="income">收入</Select.Option>
          <Select.Option value="expense">支出</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item
        name="category"
        label="分类"
        rules={[{ required: true, message: '请选择分类' }]}
      >
        <Select placeholder="请选择分类">
          {filteredCategories.map((c) => (
            <Select.Option key={c.id} value={c.name}>
              {c.name}
            </Select.Option>
          ))}
        </Select>
      </Form.Item>

      <Form.Item
        name="amount"
        label="金额"
        rules={[{ required: true, message: '请输入金额' }]}
      >
        <InputNumber
          style={{ width: '100%' }}
          min={0}
          precision={2}
          placeholder="请输入金额"
          prefix="¥"
        />
      </Form.Item>

      <Form.Item name="note" label="备注">
        <Input.TextArea rows={3} placeholder="请输入备注" />
      </Form.Item>

      <Form.Item label="凭证图片">
        <Space direction="vertical">
          {attachmentUrl && (
            <div className="mb-2">
              <img
                src={attachmentUrl}
                alt="凭证"
                style={{ maxWidth: 200, maxHeight: 200, objectFit: 'cover' }}
              />
            </div>
          )}
          <Upload {...uploadProps}>
            <Button icon={uploading ? <LoadingOutlined /> : <PlusOutlined />}>
              {uploading ? '上传中...' : '上传凭证'}
            </Button>
          </Upload>
        </Space>
      </Form.Item>

      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>
            {transaction ? '更新' : '创建'}
          </Button>
          <Button onClick={onCancel}>取消</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default TransactionForm;
