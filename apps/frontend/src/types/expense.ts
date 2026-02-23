/**
 * Dot-Store V2.2 成本记录相关类型定义
 */

/**
 * 成本记录接口
 */
export interface ExpenseRecord {
  id: number;
  user_id: number;
  category: string;
  amount: string;
  description: string | null;
  expense_date: string;
  cost_behavior: string | null;
  cost_function: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * 创建成本记录参数
 */
export interface CreateExpenseParams {
  category: string;
  amount: number | string;
  description?: string;
  expense_date: string;
  cost_behavior?: string;
  cost_function?: string;
}

/**
 * 更新成本记录参数
 */
export interface UpdateExpenseParams {
  category?: string;
  amount?: number | string;
  description?: string;
  expense_date?: string;
  cost_behavior?: string;
  cost_function?: string;
}

/**
 * 成本记录筛选条件
 */
export interface ExpenseFilters {
  category?: string;
  start_date?: string;
  end_date?: string;
  cost_behavior?: string;
  cost_function?: string;
  page?: number;
  page_size?: number;
}

/**
 * 成本记录列表响应
 */
export interface ExpenseListResponse {
  items: ExpenseRecord[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 成本汇总
 */
export interface ExpenseSummary {
  total_amount: number;
  category_breakdown: Record<string, number>;
  behavior_breakdown: Record<string, number>;
  function_breakdown: Record<string, number>;
}

/**
 * 成本分类选项
 */
export interface ExpenseCategoryOption {
  value: string;
  label: string;
}

/**
 * 成本分类列表响应
 */
export interface ExpenseCategoryListResponse {
  categories: ExpenseCategoryOption[];
  cost_behaviors: ExpenseCategoryOption[];
  cost_functions: ExpenseCategoryOption[];
}

/**
 * 成本分类选项
 */
export const EXPENSE_CATEGORY_OPTIONS: ExpenseCategoryOption[] = [
  { value: 'rent', label: '房租' },
  { value: 'labor', label: '人工' },
  { value: 'utilities', label: '水电' },
  { value: 'marketing', label: '营销' },
  { value: 'finance', label: '财务' },
  { value: 'maintenance', label: '维护' },
  { value: 'supplies', label: '耗材' },
  { value: 'other', label: '其他' },
];

/**
 * 成本行为选项
 */
export const COST_BEHAVIOR_OPTIONS: ExpenseCategoryOption[] = [
  { value: 'fixed', label: '固定成本' },
  { value: 'variable', label: '变动成本' },
  { value: 'semi_variable', label: '半变动成本' },
];

/**
 * 成本功能选项
 */
export const COST_FUNCTION_OPTIONS: ExpenseCategoryOption[] = [
  { value: 'operating', label: '运营成本' },
  { value: 'administrative', label: '管理成本' },
  { value: 'sales', label: '销售成本' },
];

/**
 * 获取成本分类显示名称
 */
export function getExpenseCategoryLabel(category: string): string {
  const option = EXPENSE_CATEGORY_OPTIONS.find(opt => opt.value === category);
  return option ? option.label : category;
}

/**
 * 获取成本行为显示名称
 */
export function getCostBehaviorLabel(behavior: string): string {
  const option = COST_BEHAVIOR_OPTIONS.find(opt => opt.value === behavior);
  return option ? option.label : behavior;
}

/**
 * 获取成本功能显示名称
 */
export function getCostFunctionLabel(func: string): string {
  const option = COST_FUNCTION_OPTIONS.find(opt => opt.value === func);
  return option ? option.label : func;
}

/**
 * 获取成本分类颜色
 */
export function getExpenseCategoryColor(category: string): string {
  const colorMap: Record<string, string> = {
    rent: '#FF4D4F',
    labor: '#FA8C16',
    utilities: '#13C2C2',
    marketing: '#722ED1',
    finance: '#1890FF',
    maintenance: '#FAAD14',
    supplies: '#52C41A',
    other: '#6B7280',
  };
  return colorMap[category] || '#6B7280';
}
