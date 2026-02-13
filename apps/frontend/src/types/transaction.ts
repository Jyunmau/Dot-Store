/**
 * 收支记录相关类型定义
 */

/**
 * 收支记录接口
 */
export interface Transaction {
  id: number;
  user_id: number;
  type: 'income' | 'expense';
  category: string;
  amount: string;
  order_id: number | null;
  note: string | null;
  attachment_url: string | null;
  created_at: string;
  updated_at: string;
  created_by: number;
}

/**
 * 收支分类接口
 */
export interface TransactionCategory {
  id: number;
  user_id: number;
  name: string;
  type: 'income' | 'expense';
  description: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * 创建收支记录参数
 */
export interface TransactionCreateParams {
  type: 'income' | 'expense';
  category: string;
  amount: number | string;
  order_id?: number;
  note?: string;
  attachment_url?: string;
}

/**
 * 更新收支记录参数
 */
export interface TransactionUpdateParams {
  category?: string;
  amount?: number | string;
  order_id?: number;
  note?: string;
  attachment_url?: string;
}

/**
 * 创建收支分类参数
 */
export interface TransactionCategoryCreateParams {
  name: string;
  type: 'income' | 'expense';
  description?: string;
}

/**
 * 更新收支分类参数
 */
export interface TransactionCategoryUpdateParams {
  name?: string;
  description?: string;
}

/**
 * 收支记录筛选条件
 */
export interface TransactionFilters {
  start_date?: string;
  end_date?: string;
  type?: 'income' | 'expense';
  category?: string;
  page?: number;
  page_size?: number;
}

/**
 * 收支记录列表响应
 */
export interface TransactionListResponse {
  items: Transaction[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 收支汇总统计
 */
export interface TransactionSummary {
  income: number;
  expense: number;
  net_profit: number;
  categories: Record<string, number>;
}

/**
 * 文件上传响应
 */
export interface UploadResponse {
  url: string;
  filename: string;
}

/**
 * 收支类型选项
 */
export const TRANSACTION_TYPE_OPTIONS = [
  { value: 'income', label: '收入', color: 'green' },
  { value: 'expense', label: '支出', color: 'red' },
];

/**
 * 默认收入分类
 */
export const DEFAULT_INCOME_CATEGORIES = [
  '堂食收入',
  '外卖收入',
  '自提收入',
  '其他收入',
];

/**
 * 默认支出分类
 */
export const DEFAULT_EXPENSE_CATEGORIES = [
  '食材采购',
  '房租水电',
  '员工工资',
  '设备维护',
  '其他支出',
];

/**
 * 获取收支类型显示名称
 */
export function getTransactionTypeLabel(type: string): string {
  const option = TRANSACTION_TYPE_OPTIONS.find((opt) => opt.value === type);
  return option ? option.label : type;
}

/**
 * 获取收支类型颜色
 */
export function getTransactionTypeColor(type: string): string {
  const option = TRANSACTION_TYPE_OPTIONS.find((opt) => opt.value === type);
  return option ? option.color : 'default';
}
