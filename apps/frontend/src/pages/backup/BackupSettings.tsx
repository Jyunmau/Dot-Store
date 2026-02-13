/**
 * 备份设置页面
 */
import React, { useEffect } from 'react';
import { Button, Form, Switch, Input, InputNumber, message, Card, Divider, Alert } from 'antd';
import { SaveOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import useBackupStore from '@/store/backupStore';
import type { BackupSettingsUpdateParams } from '@/types/backup';

/**
 * 备份设置页面组件
 */
const BackupSettings: React.FC = () => {
  const [form] = Form.useForm();

  const {
    backupSettings,
    isLoading,
    error,
    getBackupSettings,
    updateBackupSettings,
    clearError,
  } = useBackupStore();

  useEffect(() => {
    getBackupSettings();
  }, [getBackupSettings]);

  useEffect(() => {
    if (backupSettings) {
      form.setFieldsValue({
        auto_backup_enabled: backupSettings.auto_backup_enabled,
        backup_schedule: backupSettings.backup_schedule,
        backup_retention_days: backupSettings.backup_retention_days,
      });
    }
  }, [backupSettings, form]);

  useEffect(() => {
    if (error) {
      message.error(error);
      clearError();
    }
  }, [error, clearError]);

  /**
   * 处理保存设置
   */
  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      const params: BackupSettingsUpdateParams = {
        auto_backup_enabled: values.auto_backup_enabled,
        backup_schedule: values.backup_schedule,
        backup_retention_days: values.backup_retention_days,
      };

      await updateBackupSettings(params);
      message.success('备份设置保存成功');
    } catch (err) {
      console.error('保存设置失败:', err);
    }
  };

  return (
    <div className="p-6">
      <Card title="备份设置">
        <Alert
          message="自动备份功能说明"
          description="启用自动备份后，系统将按照设定的时间自动创建数据备份。备份文件将保留指定的天数，过期后自动删除。"
          type="info"
          showIcon
          className="mb-6"
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          className="max-w-lg"
        >
          <Form.Item
            name="auto_backup_enabled"
            label="启用自动备份"
            valuePropName="checked"
          >
            <Switch checkedChildren="开启" unCheckedChildren="关闭" />
          </Form.Item>

          <Form.Item
            name="backup_schedule"
            label="自动备份时间"
            rules={[{ required: true, message: '请输入备份时间' }]}
            extra={
              <span className="text-gray-500">
                使用Cron表达式，例如：0 0 * * * 表示每天凌晨执行
              </span>
            }
          >
            <Input placeholder="0 0 * * *" maxLength={128} />
          </Form.Item>

          <Form.Item
            name="backup_retention_days"
            label="备份保留天数"
            rules={[{ required: true, message: '请输入保留天数' }]}
            extra={
              <span className="text-gray-500">
                超过保留天数的自动备份将被自动删除
              </span>
            }
          >
            <InputNumber
              placeholder="请输入保留天数"
              min={1}
              max={365}
              style={{ width: '100%' }}
            />
          </Form.Item>

          {backupSettings?.last_auto_backup_at && (
            <div className="mb-6">
              <Divider />
              <p className="text-gray-600">
                最后自动备份时间：
                {dayjs(backupSettings.last_auto_backup_at).format('YYYY-MM-DD HH:mm:ss')}
              </p>
            </div>
          )}

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              icon={<SaveOutlined />}
              loading={isLoading}
            >
              保存设置
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default BackupSettings;
