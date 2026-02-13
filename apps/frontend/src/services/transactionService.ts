/**
 * 收支记录API服务
 */
import apiClient from './apiClient';
import type {
  Transaction,
  TransactionCategory,
  TransactionCreateParams,
  TransactionUpdateParams,
  TransactionCategoryCreateParams,
  TransactionCategoryUpdateParams,
  TransactionFilters,
  TransactionListResponse,
  TransactionSummary,
  UploadResponse,
} from '@/types/transaction';

/**
 * 收支记录服务对象
 */
export const transactionService = {
  /**
   * 创建收支记录
   */
  createTransaction: async (data: TransactionCreateParams): Promise<Transaction> => {
    const response = await apiClient.post<Transaction>('/transactions', data);
    return response.data;
  },

  /**
   * 获取收支记录列表
   */
  listTransactions: async (filters?: TransactionFilters): Promise<TransactionListResponse> => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.type) params.append('type', filters.type);
      if (filters.category) params.append('category', filters.category);
      if (filters.page) params.append('page', String(filters.page));
      if (filters.page_size) params.append('page_size', String(filters.page_size));
    }
    const response = await apiClient.get<TransactionListResponse>(`/transactions?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取收支记录详情
   */
  getTransaction: async (transactionId: number): Promise<Transaction> => {
    const response = await apiClient.get<Transaction>(`/transactions/${transactionId}`);
    return response.data;
  },

  /**
   * 更新收支记录
   */
  updateTransaction: async (transactionId: number, data: TransactionUpdateParams): Promise<Transaction> => {
    const response = await apiClient.put<Transaction>(`/transactions/${transactionId}`, data);
    return response.data;
  },

  /**
   * 删除收支记录
   */
  deleteTransaction: async (transactionId: number): Promise<void> => {
    await apiClient.delete(`/transactions/${transactionId}`);
  },

  /**
   * 获取收支汇总统计
   */
  getTransactionSummary: async (startDate?: string, endDate?: string): Promise<TransactionSummary> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    const response = await apiClient.get<TransactionSummary>(`/transactions/summary?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取收支分类名称列表
   */
  getCategories: async (type?: 'income' | 'expense'): Promise<string[]> => {
    const params = new URLSearchParams();
    if (type) params.append('type', type);
    const response = await apiClient.get<{ categories: string[] }>(`/transactions/categories?${params.toString()}`);
    return response.data.categories;
  },

  /**
   * 批量创建收支记录
   */
  batchCreateTransactions: async (transactions: TransactionCreateParams[]): Promise<{ created_count: number; transactions: Transaction[] }> => {
    const response = await apiClient.post<{ created_count: number; transactions: Transaction[] }>('/transactions/batch', { transactions });
    return response.data;
  },

  /**
   * 创建收支分类
   */
  createCategory: async (data: TransactionCategoryCreateParams): Promise<TransactionCategory> => {
    const response = await apiClient.post<TransactionCategory>('/transactions/categories', data);
    return response.data;
  },

  /**
   * 获取收支分类列表
   */
  listCategories: async (type?: 'income' | 'expense'): Promise<TransactionCategory[]> => {
    const params = new URLSearchParams();
    if (type) params.append('type', type);
    const response = await apiClient.get<TransactionCategory[]>(`/transactions/categories?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取收支分类详情
   */
  getCategory: async (categoryId: number): Promise<TransactionCategory> => {
    const response = await apiClient.get<TransactionCategory>(`/transactions/categories/${categoryId}`);
    return response.data;
  },

  /**
   * 更新收支分类
   */
  updateCategory: async (categoryId: number, data: TransactionCategoryUpdateParams): Promise<TransactionCategory> => {
    const response = await apiClient.put<TransactionCategory>(`/transactions/categories/${categoryId}`, data);
    return response.data;
  },

  /**
   * 删除收支分类
   */
  deleteCategory: async (categoryId: number): Promise<void> => {
    await apiClient.delete(`/transactions/categories/${categoryId}`);
  },

  /**
   * 上传凭证图片
   */
  uploadAttachment: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<UploadResponse>('/upload/attachment', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
