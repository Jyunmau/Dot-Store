/**
 * Dot-Store V2.2 现金账户服务
 */
import apiClient from './apiClient';
import type {
  CashAccount,
  CashAccountUpdateParams,
  CashTransaction,
  CashTransactionFilters,
  CashTransactionListResponse,
  RecordIncomeParams,
  RecordExpenseParams,
  CashSummary,
} from '../types/cash';

/**
 * 现金账户服务对象
 */
export const cashService = {
  /**
   * 获取现金账户
   */
  getAccount: async (): Promise<CashAccount> => {
    const response = await apiClient.get<CashAccount>('/cash/account');
    return response.data;
  },

  /**
   * 更新现金账户
   */
  updateAccount: async (data: CashAccountUpdateParams): Promise<CashAccount> => {
    const response = await apiClient.put<CashAccount>('/cash/account', data);
    return response.data;
  },

  /**
   * 记录收入
   */
  recordIncome: async (data: RecordIncomeParams): Promise<CashTransaction> => {
    const response = await apiClient.post<CashTransaction>('/cash/income', data);
    return response.data;
  },

  /**
   * 记录支出
   */
  recordExpense: async (data: RecordExpenseParams): Promise<CashTransaction> => {
    const response = await apiClient.post<CashTransaction>('/cash/expense', data);
    return response.data;
  },

  /**
   * 获取现金交易记录
   */
  getTransactions: async (filters?: CashTransactionFilters): Promise<CashTransactionListResponse> => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.start_date) params.append('start_date', filters.start_date.split('T')[0]);
      if (filters.end_date) params.append('end_date', filters.end_date.split('T')[0]);
      if (filters.transaction_type) params.append('transaction_type', filters.transaction_type);
      if (filters.category) params.append('category', filters.category);
      if (filters.page) params.append('page', String(filters.page));
      if (filters.page_size) params.append('page_size', String(filters.page_size));
    }
    const response = await apiClient.get<CashTransactionListResponse>(`/cash/transactions?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取收支汇总
   */
  getSummary: async (startDate?: string, endDate?: string): Promise<CashSummary> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate.split('T')[0]);
    if (endDate) params.append('end_date', endDate.split('T')[0]);
    const response = await apiClient.get<CashSummary>(`/cash/summary?${params.toString()}`);
    return response.data;
  },
};

export default cashService;
