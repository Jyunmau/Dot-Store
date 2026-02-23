/**
 * Dot-Store V2.2 库存相关类型定义
 */

/**
 * 食材接口
 */
export interface Ingredient {
  id: number;
  user_id: number;
  name: string;
  unit: string;
  current_stock: string;
  min_stock: string;
  cost_per_unit: string;
  warning_stock: string;
  category?: string;
  supplier?: string;
  expiry_date?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

/**
 * 库存流水接口
 */
export interface StockTransaction {
  id: number;
  user_id: number;
  ingredient_id: number;
  transaction_no: string;
  transaction_type: string;
  quantity: string;
  stock_before: string;
  stock_after: string;
  unit_cost?: string;
  total_cost?: string;
  note?: string;
  operator_id: number;
  created_at: string;
}

/**
 * 库存记录接口
 */
export interface StockRecord {
  id: number;
  ingredient_id: number;
  user_id: number;
  type: 'in' | 'out';
  quantity: string;
  note: string | null;
  created_at: string;
  ingredient_name: string | null;
  ingredient_unit: string | null;
}

/**
 * 库存预警接口
 */
export interface StockWarning {
  ingredient_id: number;
  ingredient_name: string;
  current_stock: number;
  min_stock?: number;
  expiry_date?: string;
  unit: string;
  warning_type: 'low_stock' | 'expiry';
  message: string;
}

/**
 * 库存统计接口
 */
export interface StockSummary {
  total_ingredients: number;
  low_stock_count: number;
  expiring_count: number;
  total_value: number;
}

/**
 * 创建食材参数
 */
export interface IngredientCreateParams {
  name: string;
  unit: string;
  current_stock?: number | string;
  min_stock?: number | string;
  cost_per_unit?: number | string;
  category?: string;
  supplier?: string;
  expiry_date?: string;
}

/**
 * 更新食材参数
 */
export interface IngredientUpdateParams {
  name?: string;
  unit?: string;
  current_stock?: number | string;
  min_stock?: number | string;
  cost_per_unit?: number | string;
  category?: string;
  supplier?: string;
  expiry_date?: string;
  status?: string;
}

/**
 * 入库请求参数
 */
export interface StockInParams {
  ingredient_id: number;
  quantity: number | string;
  cost?: number | string;
  note?: string;
}

/**
 * 出库请求参数
 */
export interface StockOutParams {
  ingredient_id: number;
  quantity: number | string;
  note?: string;
}

/**
 * 库存调整参数
 */
export interface StockAdjustParams {
  ingredient_id: number;
  quantity: number | string;
  note?: string;
}

/**
 * 库存记录参数（入库/出库通用）
 */
export interface StockRecordParams {
  ingredient_id: number;
  quantity: number | string;
  note?: string;
}

/**
 * 食材列表响应
 */
export interface IngredientListResponse {
  items: Ingredient[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 库存流水列表响应
 */
export interface StockTransactionListResponse {
  items: StockTransaction[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 库存记录列表响应
 */
export interface StockRecordListResponse {
  items: StockRecord[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 交易类型选项
 */
export const TRANSACTION_TYPE_OPTIONS = [
  { value: 'purchase', label: '采购入库' },
  { value: 'consume', label: '消耗出库' },
  { value: 'adjust_add', label: '盘盈' },
  { value: 'adjust_sub', label: '盘亏' },
  { value: 'return', label: '退货' },
  { value: 'transfer_in', label: '调入' },
  { value: 'transfer_out', label: '调出' },
];

/**
 * 记录类型选项
 */
export const RECORD_TYPE_OPTIONS = [
  { value: 'in', label: '入库' },
  { value: 'out', label: '出库' },
];

/**
 * 获取交易类型显示名称
 */
export function getTransactionTypeLabel(type: string): string {
  const option = TRANSACTION_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}

/**
 * 获取记录类型显示名称
 */
export function getRecordTypeLabel(type: string): string {
  const option = RECORD_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}
