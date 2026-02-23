/**
 * Dot-Store V2.2 成本记录服务
 */
import apiClient from './apiClient';
import type {
  ExpenseRecord,
  CreateExpenseParams,
  UpdateExpenseParams,
  ExpenseFilters,
  ExpenseListResponse,
  ExpenseSummary,
  ExpenseCategoryListResponse,
} from '@/types/expense';

/**
 * 成本记录服务
 */
export const expenseService = {
  /**
   * 获取成本记录列表
   */
  getExpenses: async (filters?: ExpenseFilters): Promise<ExpenseListResponse> => {
    const params = new URLSearchParams();
    
    if (filters?.category) params.append('category', filters.category);
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);
    if (filters?.cost_behavior) params.append('cost_behavior', filters.cost_behavior);
    if (filters?.cost_function) params.append('cost_function', filters.cost_function);
    if (filters?.page) params.append('page', String(filters.page));
    if (filters?.page_size) params.append('page_size', String(filters.page_size));
    
    const response = await apiClient.get<ExpenseListResponse>(`/expenses?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取成本记录详情
   */
  getExpense: async (id: number): Promise<ExpenseRecord> => {
    const response = await apiClient.get<ExpenseRecord>(`/expenses/${id}`);
    return response.data;
  },

  /**
   * 创建成本记录
   */
  createExpense: async (data: CreateExpenseParams): Promise<ExpenseRecord> => {
    const response = await apiClient.post<ExpenseRecord>('/expenses', data);
    return response.data;
  },

  /**
   * 更新成本记录
   */
  updateExpense: async (id: number, data: UpdateExpenseParams): Promise<ExpenseRecord> => {
    const response = await apiClient.put<ExpenseRecord>(`/expenses/${id}`, data);
    return response.data;
  },

  /**
   * 删除成本记录
   */
  deleteExpense: async (id: number): Promise<void> => {
    await apiClient.delete(`/expenses/${id}`);
  },

  /**
   * 获取成本汇总
   */
  getSummary: async (startDate?: string, endDate?: string): Promise<ExpenseSummary> => {
    const params = new URLSearchParams();
    
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const response = await apiClient.get<ExpenseSummary>(`/expenses/summary?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取成本分类选项
   */
  getCategories: async (): Promise<ExpenseCategoryListResponse> => {
    const response = await apiClient.get<ExpenseCategoryListResponse>('/expenses/categories');
    return response.data;
  },
};

export default expenseService;
