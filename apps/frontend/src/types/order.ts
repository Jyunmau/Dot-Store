/**
 * 订单相关类型定义
 */

/**
 * 订单接口
 */
export interface Order {
  id: number;
  user_id: number;
  amount: string;
  order_type: string;
  category_id: number | null;
  tags: string[] | null;
  order_metadata: Record<string, unknown> | null;
  status: string;
  created_at: string;
  updated_at: string;
  created_by: number;
  is_deleted: boolean;
  deleted_at: string | null;
}

/**
 * 订单分类接口
 */
export interface OrderCategory {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * 创建订单参数
 */
export interface OrderCreateParams {
  amount: number | string;
  order_type: string;
  category_id?: number;
  tags?: string[];
  order_metadata?: Record<string, unknown>;
}

/**
 * 更新订单参数
 */
export interface OrderUpdateParams {
  amount?: number | string;
  order_type?: string;
  category_id?: number;
  tags?: string[];
  order_metadata?: Record<string, unknown>;
  status?: string;
}

/**
 * 创建订单分类参数
 */
export interface OrderCategoryCreateParams {
  name: string;
  description?: string;
}

/**
 * 更新订单分类参数
 */
export interface OrderCategoryUpdateParams {
  name?: string;
  description?: string;
}

/**
 * 订单筛选条件
 */
export interface OrderFilters {
  start_date?: string;
  end_date?: string;
  order_type?: string;
  category_id?: number;
  status?: string;
  tags?: string;
  page?: number;
  page_size?: number;
}

/**
 * 订单列表响应
 */
export interface OrderListResponse {
  items: Order[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 订单类型选项
 */
export const ORDER_TYPE_OPTIONS = [
  { value: 'dine_in', label: '堂食' },
  { value: 'take_out', label: '自提' },
  { value: 'delivery', label: '外卖' },
];

/**
 * 订单状态选项
 */
export const ORDER_STATUS_OPTIONS = [
  { value: 'recorded', label: '已记录' },
  { value: 'completed', label: '已完成' },
  { value: 'cancelled', label: '已取消' },
];

/**
 * 获取订单类型显示名称
 */
export function getOrderTypeLabel(type: string): string {
  const option = ORDER_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}

/**
 * 获取订单状态显示名称
 */
export function getOrderStatusLabel(status: string): string {
  const option = ORDER_STATUS_OPTIONS.find(opt => opt.value === status);
  return option ? option.label : status;
}
