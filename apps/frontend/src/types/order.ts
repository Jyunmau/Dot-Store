/**
 * Dot-Store V2.2 订单相关类型定义
 */

/**
 * 订单类型枚举
 */
export type OrderType = 'dine_in' | 'take_out' | 'pickup';

/**
 * 支付方式枚举
 */
export type PaymentMethod = 'cash' | 'customer_account' | 'wechat' | 'alipay' | 'mixed';

/**
 * 订单接口 - V2.2
 */
export interface Order {
  id: number;
  user_id: number;
  order_no: string;
  order_type: string;
  amount: string;
  payment_method: string | null;
  customer_account_id: number | null;
  category_id: number | null;
  tags: string[] | null;
  order_metadata: Record<string, unknown> | null;
  note: string | null;
  status: string;
  is_deleted: boolean;
  deleted_at: string | null;
  deleted_by: number | null;
  created_at: string;
  updated_at: string;
  created_by: number;
}

/**
 * 订单项接口 - V2.2新增
 */
export interface OrderItem {
  id: number;
  order_id: number;
  product_name: string;
  quantity: string;
  unit_price: string;
  cost_price: string | null;
  amount: string;
  note: string | null;
  created_at: string;
}

/**
 * 订单详情响应 - V2.2新增
 */
export interface OrderDetail extends Order {
  items: OrderItem[];
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
 * 创建订单项参数 - V2.2新增
 */
export interface OrderItemCreateParams {
  product_name: string;
  quantity: number | string;
  unit_price: number | string;
  cost_price?: number | string;
  note?: string;
}

/**
 * 创建订单参数 - V2.2
 */
export interface OrderCreateParams {
  order_type: string;
  amount: number | string;
  payment_method?: string;
  customer_account_id?: number;
  category_id?: number;
  tags?: string[];
  note?: string;
  items?: OrderItemCreateParams[];
}

/**
 * 更新订单参数
 */
export interface OrderUpdateParams {
  amount?: number | string;
  order_type?: string;
  payment_method?: string;
  category_id?: number;
  tags?: string[];
  note?: string;
  status?: string;
}

/**
 * 订单作废请求参数 - V2.2新增
 */
export interface OrderVoidParams {
  reason: string;
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
 * 订单汇总 - V2.2新增
 */
export interface OrderSummary {
  total_orders: number;
  total_amount: number;
  by_type: Record<string, { count: number; amount: number }>;
  by_payment: Record<string, { count: number; amount: number }>;
}

/**
 * 订单类型选项
 */
export const ORDER_TYPE_OPTIONS = [
  { value: 'dine_in', label: '堂食' },
  { value: 'take_out', label: '自提' },
  { value: 'pickup', label: '打包' },
];

/**
 * 订单状态选项
 */
export const ORDER_STATUS_OPTIONS = [
  { value: 'completed', label: '已完成' },
  { value: 'voided', label: '已作废' },
  { value: 'cancelled', label: '已取消' },
];

/**
 * 支付方式选项 - V2.2新增
 */
export const PAYMENT_METHOD_OPTIONS = [
  { value: 'cash', label: '现金' },
  { value: 'wechat', label: '微信' },
  { value: 'alipay', label: '支付宝' },
  { value: 'customer_account', label: '会员账户' },
  { value: 'mixed', label: '混合支付' },
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

/**
 * 获取支付方式显示名称 - V2.2新增
 */
export function getPaymentMethodLabel(method: string): string {
  const option = PAYMENT_METHOD_OPTIONS.find(opt => opt.value === method);
  return option ? option.label : method || '-';
}
