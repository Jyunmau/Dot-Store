/**
 * 备份服务
 */
import apiClient from './apiClient';
import type {
  Backup,
  BackupCreateParams,
  BackupSettings,
  BackupSettingsUpdateParams,
  RestoreResult,
} from '@/types/backup';

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

/**
 * 备份API服务
 */
export const backupService = {
  /**
   * 创建备份
   */
  createBackup: async (params: BackupCreateParams): Promise<Backup> => {
    const response = await apiClient.post<ApiResponse<Backup>>('/backups', params);
    return response.data;
  },

  /**
   * 获取备份列表
   */
  getBackups: async (skip: number = 0, limit: number = 100): Promise<Backup[]> => {
    const response = await apiClient.get<ApiResponse<Backup[]>>('/backups', {
      params: { skip, limit },
    });
    return response.data;
  },

  /**
   * 获取备份详情
   */
  getBackup: async (id: number): Promise<Backup> => {
    const response = await apiClient.get<ApiResponse<Backup>>(`/backups/${id}`);
    return response.data;
  },

  /**
   * 删除备份
   */
  deleteBackup: async (id: number): Promise<void> => {
    await apiClient.delete(`/backups/${id}`);
  },

  /**
   * 下载备份
   */
  downloadBackup: async (id: number, name: string): Promise<void> => {
    const response = await apiClient.get(`/backups/${id}/download`, {
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `backup_${name}_${new Date().toISOString().split('T')[0]}.zip`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  },

  /**
   * 恢复备份
   */
  restoreBackup: async (id: number): Promise<RestoreResult> => {
    const response = await apiClient.post<ApiResponse<RestoreResult>>(`/backups/${id}/restore`);
    return response.data;
  },

  /**
   * 获取备份设置
   */
  getBackupSettings: async (): Promise<BackupSettings> => {
    const response = await apiClient.get<ApiResponse<BackupSettings>>('/backup-settings');
    return response.data;
  },

  /**
   * 更新备份设置
   */
  updateBackupSettings: async (params: BackupSettingsUpdateParams): Promise<BackupSettings> => {
    const response = await apiClient.put<ApiResponse<BackupSettings>>('/backup-settings', params);
    return response.data;
  },
};

export default backupService;
