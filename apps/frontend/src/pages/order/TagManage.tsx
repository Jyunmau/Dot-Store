/**
 * 订单标签管理页面
 */
import React, { useEffect, useState } from 'react';
import {
  Card,
  Button,
  Space,
  Tag,
  Input,
  Modal,
  message,
  Empty,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useOrderStore } from '@/store/orderStore';

/**
 * 订单标签管理页面组件
 */
const TagManagePage: React.FC = () => {
  const { orderTags, getOrderTags, isLoading } = useOrderStore();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTag, setEditingTag] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState('');
  const [localTags, setLocalTags] = useState<string[]>([]);

  useEffect(() => {
    getOrderTags();
  }, [getOrderTags]);

  useEffect(() => {
    setLocalTags(orderTags);
  }, [orderTags]);

  /**
   * 处理添加标签
   */
  const handleAdd = () => {
    setEditingTag(null);
    setInputValue('');
    setIsModalOpen(true);
  };

  /**
   * 处理编辑标签
   */
  const handleEdit = (tag: string) => {
    setEditingTag(tag);
    setInputValue(tag);
    setIsModalOpen(true);
  };

  /**
   * 处理删除标签
   */
  const handleDelete = (tag: string) => {
    setLocalTags(localTags.filter((t) => t !== tag));
    message.success('标签删除成功（仅本地删除，实际标签需在订单中修改）');
  };

  /**
   * 处理保存标签
   */
  const handleSave = () => {
    const trimmedValue = inputValue.trim();
    if (!trimmedValue) {
      message.error('标签名称不能为空');
      return;
    }

    if (editingTag) {
      if (localTags.includes(trimmedValue) && trimmedValue !== editingTag) {
        message.error('标签已存在');
        return;
      }
      setLocalTags(localTags.map((t) => (t === editingTag ? trimmedValue : t)));
      message.success('标签更新成功（仅本地更新，实际标签需在订单中修改）');
    } else {
      if (localTags.includes(trimmedValue)) {
        message.error('标签已存在');
        return;
      }
      setLocalTags([...localTags, trimmedValue]);
      message.success('标签添加成功（仅本地添加，实际标签需在订单中创建）');
    }

    setIsModalOpen(false);
    setEditingTag(null);
    setInputValue('');
  };

  return (
    <div className="p-6">
      <Card
        title="订单标签管理"
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新增标签
          </Button>
        }
      >
        <div className="mb-4 text-gray-500">
          提示：标签来源于订单数据，此处仅提供查看和管理功能。如需创建新标签，请在订单中添加。
        </div>

        {localTags.length === 0 && !isLoading ? (
          <Empty description="暂无标签" />
        ) : (
          <Space size={[8, 16]} wrap>
            {localTags.map((tag) => (
              <Tag
                key={tag}
                style={{
                  padding: '4px 8px',
                  fontSize: '14px',
                  border: '1px solid #d9d9d9',
                }}
              >
                <Space size={4}>
                  <span>{tag}</span>
                  <EditOutlined
                    style={{ cursor: 'pointer', color: '#1890ff' }}
                    onClick={() => handleEdit(tag)}
                  />
                  <DeleteOutlined
                    style={{ cursor: 'pointer', color: '#ff4d4f' }}
                    onClick={() => handleDelete(tag)}
                  />
                </Space>
              </Tag>
            ))}
          </Space>
        )}
      </Card>

      <Modal
        title={editingTag ? '编辑标签' : '新增标签'}
        open={isModalOpen}
        onOk={handleSave}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingTag(null);
          setInputValue('');
        }}
        okText="保存"
        cancelText="取消"
      >
        <Input
          placeholder="请输入标签名称"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          maxLength={32}
          showCount
        />
      </Modal>
    </div>
  );
};

export default TagManagePage;
