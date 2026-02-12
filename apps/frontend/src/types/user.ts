/**
 * 用户相关类型定义
 */

export interface User {
  id: number;
  phone: string | null;
  email: string | null;
  shop_name: string;
  shop_type: string;
  city: string;
  role: string;
  status: string;
  created_at: string;
  last_login_at: string | null;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  phone?: string;
  email?: string;
  password: string;
  shop_name: string;
  shop_type: string;
  city: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface Staff {
  id: number;
  phone: string | null;
  email: string | null;
  shop_name: string;
  role: string;
  status: string;
  permissions: string[];
  created_at: string;
}

export interface CreateStaffRequest {
  phone?: string;
  email?: string;
  password: string;
  shop_name?: string;
}

export interface UpdatePermissionRequest {
  permissions: string[];
}

export interface PermissionGroup {
  name: string;
  permissions: {
    key: string;
    name: string;
  }[];
}

export interface PermissionGroups {
  [key: string]: PermissionGroup;
}
