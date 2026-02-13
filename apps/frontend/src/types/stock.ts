/**
 * 库存相关类型定义
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
  warning_stock: string;
  created_at: string;
  updated_at: string;
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
  name: string;
  unit: string;
  current_stock: string;
  warning_stock: string;
  deficit: string;
}

/**
 * 库存统计接口
 */
export interface StockSummary {
  total_ingredients: number;
  low_stock_count: number;
  total_value: string;
}

/**
 * 创建食材参数
 */
export interface IngredientCreateParams {
  name: string;
  unit: string;
  current_stock?: number | string;
  warning_stock?: number | string;
}

/**
 * 更新食材参数
 */
export interface IngredientUpdateParams {
  name?: string;
  unit?: string;
  current_stock?: number | string;
  warning_stock?: number | string;
}

/**
 * 库存记录参数
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
 * 库存记录列表响应
 */
export interface StockRecordListResponse {
  items: StockRecord[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 记录类型选项
 */
export const RECORD_TYPE_OPTIONS = [
  { value: 'in', label: '入库' },
  { value: 'out', label: '出库' },
];

/**
 * 获取记录类型显示名称
 */
export function getRecordTypeLabel(type: string): string {
  const option = RECORD_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}
