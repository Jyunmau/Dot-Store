/**
 * 备份状态管理
 */
import { create } from 'zustand';
import type {
  Backup,
  BackupCreateParams,
  BackupSettings,
  BackupSettingsUpdateParams,
  RestoreResult,
} from '@/types/backup';
import backupService from '@/services/backupService';

interface BackupState {
  backups: Backup[];
  currentBackup: Backup | null;
  backupSettings: BackupSettings | null;
  isLoading: boolean;
  error: string | null;

  getBackups: () => Promise<void>;
  createBackup: (params: BackupCreateParams) => Promise<Backup>;
  deleteBackup: (id: number) => Promise<void>;
  downloadBackup: (id: number, name: string) => Promise<void>;
  restoreBackup: (id: number) => Promise<RestoreResult>;
  getBackupSettings: () => Promise<void>;
  updateBackupSettings: (params: BackupSettingsUpdateParams) => Promise<void>;
  clearError: () => void;
}

const useBackupStore = create<BackupState>((set) => ({
  backups: [],
  currentBackup: null,
  backupSettings: null,
  isLoading: false,
  error: null,

  getBackups: async () => {
    set({ isLoading: true, error: null });
    try {
      const backups = await backupService.getBackups();
      set({ backups, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取备份列表失败',
        isLoading: false,
      });
    }
  },

  createBackup: async (params: BackupCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const backup = await backupService.createBackup(params);
      set((state) => ({
        backups: [backup, ...state.backups],
        isLoading: false,
      }));
      return backup;
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '创建备份失败',
        isLoading: false,
      });
      throw error;
    }
  },

  deleteBackup: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      await backupService.deleteBackup(id);
      set((state) => ({
        backups: state.backups.filter((backup) => backup.id !== id),
        isLoading: false,
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '删除备份失败',
        isLoading: false,
      });
      throw error;
    }
  },

  downloadBackup: async (id: number, name: string) => {
    set({ isLoading: true, error: null });
    try {
      await backupService.downloadBackup(id, name);
      set({ isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '下载备份失败',
        isLoading: false,
      });
      throw error;
    }
  },

  restoreBackup: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      const result = await backupService.restoreBackup(id);
      set({ isLoading: false });
      return result;
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '恢复备份失败',
        isLoading: false,
      });
      throw error;
    }
  },

  getBackupSettings: async () => {
    set({ isLoading: true, error: null });
    try {
      const settings = await backupService.getBackupSettings();
      set({ backupSettings: settings, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取备份设置失败',
        isLoading: false,
      });
    }
  },

  updateBackupSettings: async (params: BackupSettingsUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const settings = await backupService.updateBackupSettings(params);
      set({ backupSettings: settings, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '更新备份设置失败',
        isLoading: false,
      });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));

export default useBackupStore;
