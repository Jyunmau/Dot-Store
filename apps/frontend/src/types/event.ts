/**
 * Dot-Store V2.2 事件日志类型定义
 */

export type EventCategory = 'auth' | 'order' | 'stock' | 'customer' | 'cash' | 'finance' | 'system' | 'mcp';

export type EventType =
  | 'user_login'
  | 'user_logout'
  | 'user_register'
  | 'api_key_generated'
  | 'order_created'
  | 'order_updated'
  | 'order_voided'
  | 'stock_in'
  | 'stock_out'
  | 'stock_adjust'
  | 'ingredient_created'
  | 'customer_created'
  | 'customer_recharge'
  | 'customer_consume'
  | 'cash_income'
  | 'cash_expense'
  | 'financial_snapshot_created'
  | 'backup_created'
  | 'backup_restored'
  | 'mcp_tool_called'
  | 'mcp_resource_accessed';

export interface BusinessEvent {
  id: number;
  user_id: number;
  event_type: EventType;
  event_category: EventCategory;
  entity_type?: string;
  entity_id?: number;
  operator_id: number;
  operator_type: 'user' | 'system' | 'mcp';
  data?: Record<string, any>;
  ip_address?: string;
  created_at: string;
}

export interface EventListResponse {
  items: BusinessEvent[];
  total: number;
  page: number;
  page_size: number;
}

export interface EventQueryParams {
  start_date?: string;
  end_date?: string;
  event_type?: string;
  event_category?: string;
  entity_type?: string;
  entity_id?: number;
  page?: number;
  page_size?: number;
}

export const EVENT_CATEGORY_LABELS: Record<EventCategory, string> = {
  auth: '认证',
  order: '订单',
  stock: '库存',
  customer: '客户',
  cash: '现金',
  finance: '财务',
  system: '系统',
  mcp: 'MCP',
};

export const EVENT_CATEGORY_COLORS: Record<EventCategory, string> = {
  auth: 'blue',
  order: 'green',
  stock: 'orange',
  customer: 'purple',
  cash: 'cyan',
  finance: 'gold',
  system: 'default',
  mcp: 'magenta',
};

export const EVENT_TYPE_LABELS: Record<EventType, string> = {
  user_login: '用户登录',
  user_logout: '用户登出',
  user_register: '用户注册',
  api_key_generated: 'API密钥生成',
  order_created: '订单创建',
  order_updated: '订单更新',
  order_voided: '订单作废',
  stock_in: '入库',
  stock_out: '出库',
  stock_adjust: '库存调整',
  ingredient_created: '食材创建',
  customer_created: '客户创建',
  customer_recharge: '客户充值',
  customer_consume: '客户消费',
  cash_income: '现金收入',
  cash_expense: '现金支出',
  financial_snapshot_created: '财务快照创建',
  backup_created: '备份创建',
  backup_restored: '备份恢复',
  mcp_tool_called: 'MCP工具调用',
  mcp_resource_accessed: 'MCP资源访问',
};
