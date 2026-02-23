/**
 * Dot-Store V2.2 客户账户服务
 */
import apiClient from './apiClient';
import type {
  CustomerAccount,
  CustomerAccountCreateParams,
  CustomerAccountUpdateParams,
  CustomerAccountFilters,
  CustomerAccountListResponse,
  CustomerTransaction,
  CustomerTransactionFilters,
  CustomerTransactionListResponse,
  RechargeParams,
  ConsumeParams,
  RebuildBalanceResponse,
} from '../types/customer';

/**
 * 客户账户服务对象
 */
export const customerService = {
  /**
   * 创建客户账户
   */
  createAccount: async (data: CustomerAccountCreateParams): Promise<CustomerAccount> => {
    const response = await apiClient.post<CustomerAccount>('/customers', data);
    return response.data;
  },

  /**
   * 获取客户账户列表
   */
  listAccounts: async (filters?: CustomerAccountFilters): Promise<CustomerAccountListResponse> => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.search) params.append('search', filters.search);
      if (filters.status) params.append('status', filters.status);
      if (filters.page) params.append('page', String(filters.page));
      if (filters.page_size) params.append('page_size', String(filters.page_size));
    }
    const response = await apiClient.get<CustomerAccountListResponse>(`/customers?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取客户账户详情
   */
  getAccount: async (accountId: number): Promise<CustomerAccount> => {
    const response = await apiClient.get<CustomerAccount>(`/customers/${accountId}`);
    return response.data;
  },

  /**
   * 按手机号查询客户账户
   */
  getAccountByPhone: async (phone: string): Promise<CustomerAccount> => {
    const response = await apiClient.get<CustomerAccount>(`/customers/phone/${phone}`);
    return response.data;
  },

  /**
   * 更新客户账户
   */
  updateAccount: async (accountId: number, data: CustomerAccountUpdateParams): Promise<CustomerAccount> => {
    const response = await apiClient.put<CustomerAccount>(`/customers/${accountId}`, data);
    return response.data;
  },

  /**
   * 客户充值
   */
  recharge: async (accountId: number, data: RechargeParams): Promise<CustomerTransaction> => {
    const response = await apiClient.post<CustomerTransaction>(`/customers/${accountId}/recharge`, data);
    return response.data;
  },

  /**
   * 客户消费
   */
  consume: async (accountId: number, data: ConsumeParams): Promise<CustomerTransaction> => {
    const response = await apiClient.post<CustomerTransaction>(`/customers/${accountId}/consume`, data);
    return response.data;
  },

  /**
   * 获取客户交易记录
   */
  getTransactions: async (accountId: number, filters?: CustomerTransactionFilters): Promise<CustomerTransactionListResponse> => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.transaction_type) params.append('transaction_type', filters.transaction_type);
      if (filters.start_date) params.append('start_date', filters.start_date.split('T')[0]);
      if (filters.end_date) params.append('end_date', filters.end_date.split('T')[0]);
      if (filters.page) params.append('page', String(filters.page));
      if (filters.page_size) params.append('page_size', String(filters.page_size));
    }
    const response = await apiClient.get<CustomerTransactionListResponse>(`/customers/${accountId}/transactions?${params.toString()}`);
    return response.data;
  },

  /**
   * 重建余额
   */
  rebuildBalance: async (accountId: number): Promise<RebuildBalanceResponse> => {
    const response = await apiClient.post<RebuildBalanceResponse>(`/customers/${accountId}/rebuild-balance`);
    return response.data;
  },
};

export default customerService;
