/**
 * 报表相关类型定义
 */

/**
 * 每日数据类型
 */
export interface DailyData {
  date: string;
  income: number;
  expense: number;
  profit: number;
}

/**
 * 每周数据类型
 */
export interface WeeklyData {
  week: number;
  income: number;
  expense: number;
  profit: number;
}

/**
 * 报表数据类型
 */
export interface ReportData {
  date?: string;
  start_date?: string;
  end_date?: string;
  year?: number;
  month?: number;
  income: number;
  expense: number;
  profit: number;
  order_count: number;
  order_amount: number;
  income_categories: Record<string, number>;
  expense_categories: Record<string, number>;
  daily_data?: DailyData[];
  weekly_data?: WeeklyData[];
}

/**
 * 报表筛选条件类型
 */
export interface ReportFilters {
  start_date: string;
  end_date: string;
  type: string;
  categories?: string[];
}

/**
 * 分类分析数据类型
 */
export interface CategoryAnalysis {
  type: string;
  categories: Record<string, number>;
  total: number;
}

/**
 * 导出请求类型
 */
export interface ExportRequest {
  report_data: ReportData;
  report_type: string;
}

/**
 * 报表类型枚举
 */
export type ReportType = 'daily' | 'weekly' | 'monthly' | 'custom';

/**
 * 导出格式枚举
 */
export type ExportFormat = 'excel' | 'pdf';
