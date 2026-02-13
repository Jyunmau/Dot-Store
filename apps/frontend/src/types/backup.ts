/**
 * 备份相关类型定义
 */

/**
 * 备份状态
 */
export type BackupStatus = 'pending' | 'in_progress' | 'completed' | 'failed';

/**
 * 备份类型
 */
export type BackupType = 'manual' | 'auto';

/**
 * 备份记录
 */
export interface Backup {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  status: BackupStatus;
  backup_path: string;
  backup_size: number;
  backup_type: BackupType;
  created_at: string;
  completed_at: string | null;
}

/**
 * 创建备份参数
 */
export interface BackupCreateParams {
  name: string;
  description?: string;
}

/**
 * 备份设置
 */
export interface BackupSettings {
  id: number;
  user_id: number;
  auto_backup_enabled: boolean;
  backup_schedule: string;
  backup_retention_days: number;
  last_auto_backup_at: string | null;
  updated_at: string;
}

/**
 * 更新备份设置参数
 */
export interface BackupSettingsUpdateParams {
  auto_backup_enabled: boolean;
  backup_schedule: string;
  backup_retention_days: number;
}

/**
 * 恢复结果
 */
export interface RestoreResult {
  message: string;
  restored_counts: {
    orders: number;
    order_categories: number;
    transactions: number;
    transaction_categories: number;
  };
}
