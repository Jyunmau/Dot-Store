/**
 * Dot-Store V2.2 现金流分析类型定义
 */

/**
 * 三色安全指数
 */
export interface SafetyIndex {
  safety_score: number;
  safety_level: 'safe' | 'warning' | 'danger';
  color_code: string;
  message: string;
  factors: {
    cash_balance: number;
    liability: number;
    net_available: number;
    days_of_operation: number;
  };
}

/**
 * 现金流分析
 */
export interface CashFlowAnalysis {
  id: number;
  user_id: number;
  analysis_date: string;
  analysis_type: string;
  period_start: string;
  period_end: string;
  total_income: number;
  total_expense: number;
  net_cash_flow: number;
  avg_daily_income: number;
  avg_daily_expense: number;
  income_structure: Record<string, number>;
  expense_structure: Record<string, number>;
  health_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  recommendations?: string[];
  created_at: string;
}

/**
 * 现金流预测
 */
export interface CashFlowForecast {
  id: number;
  user_id: number;
  forecast_date: string;
  target_date: string;
  predicted_income: number;
  predicted_expense: number;
  predicted_balance: number;
  confidence_level: number;
  risk_alert: boolean;
  alert_message?: string;
  created_at: string;
}

/**
 * 现金流预测列表响应
 */
export interface CashFlowForecastListResponse {
  items: CashFlowForecast[];
  total: number;
}

/**
 * 风险预警
 */
export interface RiskAlert {
  id: number;
  user_id: number;
  alert_date: string;
  alert_level: 'low' | 'medium' | 'high' | 'critical';
  alert_type: string;
  message: string;
  suggestions?: string[];
  is_read: boolean;
  is_resolved: boolean;
  resolved_at?: string;
  created_at: string;
}

/**
 * 风险预警列表响应
 */
export interface RiskAlertListResponse {
  items: RiskAlert[];
  total: number;
  unread_count: number;
}

/**
 * 收入结构响应
 */
export interface IncomeStructureResponse {
  total_income: number;
  income_by_category: Record<string, number>;
  income_by_mode: Record<string, number>;
  income_trend: Array<{
    date: string;
    amount: number;
  }>;
  stability_score: number;
  growth_rate?: number;
}

/**
 * 支出结构响应
 */
export interface ExpenseStructureResponse {
  total_expense: number;
  expense_by_category: Record<string, number>;
  expense_by_behavior: Record<string, number>;
  expense_by_function: Record<string, number>;
  expense_trend: Array<{
    date: string;
    amount: number;
  }>;
  anomaly_detected: boolean;
}

/**
 * 盈亏平衡分析
 */
export interface BreakEvenAnalysis {
  break_even_point: number;
  current_revenue: number;
  fixed_cost: number;
  variable_cost_ratio: number;
  contribution_margin_ratio: number;
  safety_margin: number;
  safety_margin_ratio: number;
  status: 'profit' | 'loss' | 'break_even';
}

/**
 * 月度健康报告
 */
export interface MonthlyReport {
  year: number;
  month: number;
  period_start: string;
  period_end: string;
  total_income: number;
  total_expense: number;
  net_cash_flow: number;
  income_structure: IncomeStructureResponse;
  expense_structure: ExpenseStructureResponse;
  break_even: BreakEvenAnalysis;
  safety_index: SafetyIndex;
  health_score: number;
  risk_level: string;
  recommendations: string[];
  action_items: string[];
  comparison?: {
    cash_balance_change: number;
    inventory_value_change: number;
    prepaid_balance_change: number;
  };
}

/**
 * 收入波动归因
 */
export interface IncomeVolatility {
  volatility_score: number;
  trend: 'up' | 'down' | 'stable';
  change_percentage: number;
  factors: Array<{
    category: string;
    amount: number;
    percentage: number;
  }>;
  main_cause: string;
  suggestions: string[];
}

/**
 * 仪表盘数据
 */
export interface DashboardData {
  safety_index: SafetyIndex;
  current_balance: number;
  yesterday_change: number;
  monthly_income: number;
  monthly_expense: number;
  monthly_profit: number;
  recent_trend: Array<{
    date: string;
    income: number;
    expense: number;
  }>;
  active_alerts: Array<{
    id: number;
    alert_level: string;
    alert_type: string;
    message: string;
    created_at: string;
  }>;
  forecast_summary: {
    has_risk: boolean;
    predicted_balance_end: number;
    avg_daily_income: number;
    avg_daily_expense: number;
  };
}

/**
 * 用户偏好配置
 */
export interface UserPreference {
  id: number;
  user_id: number;
  weekly_reminder_enabled: boolean;
  weekly_reminder_day: number;
  weekly_reminder_time: string;
  monthly_report_enabled: boolean;
  monthly_report_day: number;
  monthly_report_time: string;
  risk_alert_enabled: boolean;
  risk_alert_threshold: 'low' | 'medium' | 'high';
  notification_channels: string[];
}
