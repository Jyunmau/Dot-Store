/**
 * Dot-Store V2.2 客户账户相关类型定义
 */

/**
 * 客户账户接口
 */
export interface CustomerAccount {
  id: number;
  user_id: number;
  customer_name: string;
  phone: string;
  balance: string;
  total_recharged: string;
  total_consumed: string;
  status: string;
  created_at: string;
  updated_at: string;
}

/**
 * 客户交易接口
 */
export interface CustomerTransaction {
  id: number;
  user_id: number;
  account_id: number;
  transaction_no: string;
  transaction_type: string;
  amount: string;
  balance_before: string;
  balance_after: string;
  order_id: number | null;
  note: string | null;
  operator_id: number;
  created_at: string;
}

/**
 * 创建客户账户参数
 */
export interface CustomerAccountCreateParams {
  customer_name: string;
  phone: string;
}

/**
 * 更新客户账户参数
 */
export interface CustomerAccountUpdateParams {
  customer_name?: string;
  status?: string;
}

/**
 * 充值请求参数
 */
export interface RechargeParams {
  amount: number | string;
  note?: string;
}

/**
 * 消费请求参数
 */
export interface ConsumeParams {
  amount: number | string;
  order_id?: number;
  note?: string;
}

/**
 * 客户账户筛选条件
 */
export interface CustomerAccountFilters {
  search?: string;
  status?: string;
  page?: number;
  page_size?: number;
}

/**
 * 客户交易筛选条件
 */
export interface CustomerTransactionFilters {
  transaction_type?: string;
  start_date?: string;
  end_date?: string;
  page?: number;
  page_size?: number;
}

/**
 * 客户账户列表响应
 */
export interface CustomerAccountListResponse {
  items: CustomerAccount[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 客户交易列表响应
 */
export interface CustomerTransactionListResponse {
  items: CustomerTransaction[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 重建余额响应
 */
export interface RebuildBalanceResponse {
  account_id: number;
  original_balance: string;
  calculated_balance: string;
  is_consistent: boolean;
}

/**
 * 交易类型选项
 */
export const CUSTOMER_TRANSACTION_TYPE_OPTIONS = [
  { value: 'recharge', label: '充值' },
  { value: 'consume', label: '消费' },
  { value: 'refund', label: '退款' },
  { value: 'adjust_add', label: '调整增加' },
  { value: 'adjust_sub', label: '调整减少' },
];

/**
 * 客户账户状态选项
 */
export const CUSTOMER_ACCOUNT_STATUS_OPTIONS = [
  { value: 'active', label: '正常' },
  { value: 'inactive', label: '停用' },
  { value: 'frozen', label: '冻结' },
];

/**
 * 获取交易类型显示名称
 */
export function getCustomerTransactionTypeLabel(type: string): string {
  const option = CUSTOMER_TRANSACTION_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}

/**
 * 获取账户状态显示名称
 */
export function getCustomerAccountStatusLabel(status: string): string {
  const option = CUSTOMER_ACCOUNT_STATUS_OPTIONS.find(opt => opt.value === status);
  return option ? option.label : status;
}

/**
 * 获取交易类型颜色
 */
export function getCustomerTransactionTypeColor(type: string): string {
  const colorMap: Record<string, string> = {
    recharge: '#52C41A',
    consume: '#1890FF',
    refund: '#FAAD14',
    adjust_add: '#52C41A',
    adjust_sub: '#FF4D4F',
  };
  return colorMap[type] || '#6B7280';
}
