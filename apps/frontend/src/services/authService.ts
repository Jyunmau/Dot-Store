/**
 * 认证服务
 */
import apiClient from './apiClient';
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User,
  Staff,
  CreateStaffRequest,
  UpdatePermissionRequest,
  PermissionGroups,
} from '@/types/user';

export const authService = {
  /**
   * 用户登录
   */
  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/login', data);
    return response.data;
  },

  /**
   * 用户注册
   */
  async register(data: RegisterRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/register', data);
    return response.data;
  },

  /**
   * 用户登出
   */
  async logout(): Promise<void> {
    await apiClient.post('/auth/logout');
  },

  /**
   * 刷新令牌
   */
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  /**
   * 获取当前用户信息
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/users/me');
    return response.data;
  },

  /**
   * 添加店员
   */
  async createStaff(data: CreateStaffRequest): Promise<Staff> {
    const response = await apiClient.post<Staff>('/auth/staff', data);
    return response.data;
  },

  /**
   * 获取店员列表
   */
  async getStaffList(): Promise<Staff[]> {
    const response = await apiClient.get<Staff[]>('/auth/staff');
    return response.data;
  },

  /**
   * 获取店员详情
   */
  async getStaffDetail(staffId: number): Promise<Staff> {
    const response = await apiClient.get<Staff>(`/auth/staff/${staffId}`);
    return response.data;
  },

  /**
   * 更新店员权限
   */
  async updateStaffPermissions(staffId: number, data: UpdatePermissionRequest): Promise<Staff> {
    const response = await apiClient.put<Staff>(`/auth/staff/${staffId}/permissions`, data);
    return response.data;
  },

  /**
   * 移除店员
   */
  async removeStaff(staffId: number): Promise<void> {
    await apiClient.delete(`/auth/staff/${staffId}`);
  },
};

export const permissionService = {
  /**
   * 获取权限分组
   */
  async getPermissionGroups(): Promise<PermissionGroups> {
    const response = await apiClient.get<PermissionGroups>('/permission/groups');
    return response.data;
  },

  /**
   * 获取当前用户权限
   */
  async getMyPermissions(): Promise<{ role: string; permissions: string[] }> {
    const response = await apiClient.get<{ role: string; permissions: string[] }>('/permission/me');
    return response.data;
  },

  /**
   * 检查权限
   */
  async checkPermission(permission: string): Promise<{ permission: string; has_permission: boolean }> {
    const response = await apiClient.get<{ permission: string; has_permission: boolean }>('/permission/check', {
      params: { permission },
    });
    return response.data;
  },
};
