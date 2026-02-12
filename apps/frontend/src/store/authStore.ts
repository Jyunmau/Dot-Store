/**
 * 认证状态管理
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types/user';
import { authService } from '@/services/authService';

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: string | null;
  
  login: (username: string, password: string) => Promise<void>;
  register: (data: {
    phone?: string;
    email?: string;
    password: string;
    shop_name: string;
    shop_type: string;
    city: string;
  }) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  setToken: (token: string, refreshToken: string) => void;
  clearError: () => void;
  refreshAccessToken: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      isAuthenticated: false,
      user: null,
      token: null,
      refreshToken: null,
      loading: false,
      error: null,

      login: async (username: string, password: string) => {
        set({ loading: true, error: null });
        try {
          const response = await authService.login({ username, password });
          set({
            isAuthenticated: true,
            user: response.user,
            token: response.access_token,
            refreshToken: response.refresh_token,
            loading: false,
          });
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : '登录失败';
          set({ error: errorMessage, loading: false });
          throw error;
        }
      },

      register: async (data) => {
        set({ loading: true, error: null });
        try {
          const response = await authService.register(data);
          set({
            isAuthenticated: true,
            user: response.user,
            token: response.access_token,
            refreshToken: response.refresh_token,
            loading: false,
          });
        } catch (error: unknown) {
          const errorMessage = error instanceof Error ? error.message : '注册失败';
          set({ error: errorMessage, loading: false });
          throw error;
        }
      },

      logout: () => {
        set({
          isAuthenticated: false,
          user: null,
          token: null,
          refreshToken: null,
          error: null,
        });
      },

      setUser: (user: User) => {
        set({ user });
      },

      setToken: (token: string, refreshToken: string) => {
        set({ token, refreshToken });
      },

      clearError: () => {
        set({ error: null });
      },

      refreshAccessToken: async () => {
        const { refreshToken } = get();
        if (!refreshToken) {
          throw new Error('没有刷新令牌');
        }
        try {
          const response = await authService.refreshToken(refreshToken);
          set({
            token: response.access_token,
            refreshToken: response.refresh_token,
          });
        } catch (error) {
          get().logout();
          throw error;
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
