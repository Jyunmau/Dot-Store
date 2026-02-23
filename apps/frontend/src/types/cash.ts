/**
 * Dot-Store V2.2 现金账户相关类型定义
 */

/**
 * 现金账户接口
 */
export interface CashAccount {
  id: number;
  user_id: number;
  account_name: string;
  account_type: string;
  balance: string;
  total_income: string;
  total_expense: string;
  status: string;
  created_at: string;
  updated_at: string;
}

/**
 * 现金交易接口
 */
export interface CashTransaction {
  id: number;
  user_id: number;
  account_id: number;
  transaction_no: string;
  transaction_type: string;
  category: string;
  amount: string;
  balance_before: string;
  balance_after: string;
  order_id: number | null;
  customer_transaction_id: number | null;
  note: string | null;
  operator_id: number;
  created_at: string;
}

/**
 * 更新现金账户参数
 */
export interface CashAccountUpdateParams {
  account_name?: string;
}

/**
 * 记录收入参数
 */
export interface RecordIncomeParams {
  amount: number | string;
  category: string;
  order_id?: number;
  customer_transaction_id?: number;
  note?: string;
}

/**
 * 记录支出参数
 */
export interface RecordExpenseParams {
  amount: number | string;
  category: string;
  note?: string;
}

/**
 * 现金交易筛选条件
 */
export interface CashTransactionFilters {
  start_date?: string;
  end_date?: string;
  transaction_type?: string;
  category?: string;
  page?: number;
  page_size?: number;
}

/**
 * 现金交易列表响应
 */
export interface CashTransactionListResponse {
  items: CashTransaction[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 现金收支汇总
 */
export interface CashSummary {
  total_income: number;
  total_expense: number;
  net_income: number;
  categories: Record<string, number>;
}

/**
 * 交易类型选项
 */
export const CASH_TRANSACTION_TYPE_OPTIONS = [
  { value: 'income', label: '收入' },
  { value: 'expense', label: '支出' },
  { value: 'transfer_in', label: '转入' },
  { value: 'transfer_out', label: '转出' },
  { value: 'adjust_add', label: '调整增加' },
  { value: 'adjust_sub', label: '调整减少' },
];

/**
 * 收入分类选项
 */
export const INCOME_CATEGORY_OPTIONS = [
  { value: 'order_income', label: '订单收入' },
  { value: 'recharge_income', label: '充值收入' },
  { value: 'refund_income', label: '退款收入' },
  { value: 'other_income', label: '其他收入' },
];

/**
 * 支出分类选项
 */
export const EXPENSE_CATEGORY_OPTIONS = [
  { value: 'purchase', label: '采购支出' },
  { value: 'salary', label: '工资支出' },
  { value: 'rent', label: '房租支出' },
  { value: 'utility', label: '水电费' },
  { value: 'other_expense', label: '其他支出' },
];

/**
 * 获取交易类型显示名称
 */
export function getCashTransactionTypeLabel(type: string): string {
  const option = CASH_TRANSACTION_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}

/**
 * 获取收支分类显示名称
 */
export function getCashCategoryLabel(category: string): string {
  const incomeOption = INCOME_CATEGORY_OPTIONS.find(opt => opt.value === category);
  if (incomeOption) return incomeOption.label;
  
  const expenseOption = EXPENSE_CATEGORY_OPTIONS.find(opt => opt.value === category);
  if (expenseOption) return expenseOption.label;
  
  return category;
}

/**
 * 获取交易类型颜色
 */
export function getCashTransactionTypeColor(type: string): string {
  const colorMap: Record<string, string> = {
    income: '#52C41A',
    expense: '#FF4D4F',
    transfer_in: '#1890FF',
    transfer_out: '#FAAD14',
    adjust_add: '#52C41A',
    adjust_sub: '#FF4D4F',
  };
  return colorMap[type] || '#6B7280';
}
