/**
 * Dot-Store V2.2 现金流分析服务
 */
import apiClient from './apiClient';
import type {
  SafetyIndex,
  CashFlowAnalysis,
  CashFlowForecastListResponse,
  RiskAlertListResponse,
  RiskAlert,
  IncomeStructureResponse,
  ExpenseStructureResponse,
  BreakEvenAnalysis,
  DashboardData,
  MonthlyReport,
  IncomeVolatility,
  UserPreference,
} from '@/types/cashFlow';

/**
 * 现金流分析服务
 */
export const cashFlowService = {
  /**
   * 获取三色安全指数
   */
  async getSafetyIndex(): Promise<SafetyIndex> {
    const response = await apiClient.get<SafetyIndex>('/cashflow/safety-index');
    return response.data;
  },

  /**
   * 执行现金流分析
   */
  async analyzeCashFlow(
    periodStart: string,
    periodEnd: string,
    analysisType: string = 'monthly'
  ): Promise<CashFlowAnalysis> {
    const response = await apiClient.post<CashFlowAnalysis>('/cashflow/analyze', {
      period_start: periodStart,
      period_end: periodEnd,
      analysis_type: analysisType,
    });
    return response.data;
  },

  /**
   * 获取现金流预测
   */
  async getForecast(days: number = 30): Promise<CashFlowForecastListResponse> {
    const response = await apiClient.get<CashFlowForecastListResponse>('/cashflow/forecast', {
      params: { days },
    });
    return response.data;
  },

  /**
   * 获取收入结构分析
   */
  async getIncomeStructure(
    periodStart: string,
    periodEnd: string
  ): Promise<IncomeStructureResponse> {
    const response = await apiClient.get<IncomeStructureResponse>('/cashflow/income-structure', {
      params: {
        period_start: periodStart,
        period_end: periodEnd,
      },
    });
    return response.data;
  },

  /**
   * 获取支出结构分析
   */
  async getExpenseStructure(
    periodStart: string,
    periodEnd: string
  ): Promise<ExpenseStructureResponse> {
    const response = await apiClient.get<ExpenseStructureResponse>('/cashflow/expense-structure', {
      params: {
        period_start: periodStart,
        period_end: periodEnd,
      },
    });
    return response.data;
  },

  /**
   * 获取盈亏平衡分析
   */
  async getBreakEvenAnalysis(): Promise<BreakEvenAnalysis> {
    const response = await apiClient.get<BreakEvenAnalysis>('/cashflow/break-even');
    return response.data;
  },

  /**
   * 获取月度健康报告
   */
  async getMonthlyReport(year: number, month: number): Promise<MonthlyReport> {
    const response = await apiClient.get<MonthlyReport>('/cashflow/monthly-report', {
      params: { year, month },
    });
    return response.data;
  },

  /**
   * 获取收入波动归因
   */
  async getIncomeVolatility(): Promise<IncomeVolatility> {
    const response = await apiClient.get<IncomeVolatility>('/cashflow/income-volatility');
    return response.data;
  },

  /**
   * 获取仪表盘数据
   */
  async getDashboard(): Promise<DashboardData> {
    const response = await apiClient.get<DashboardData>('/cashflow/dashboard');
    return response.data;
  },
};

/**
 * 风险预警服务
 */
export const riskAlertService = {
  /**
   * 获取风险预警列表
   */
  async getAlerts(
    includeResolved: boolean = false,
    level?: string,
    limit: number = 20,
    offset: number = 0
  ): Promise<RiskAlertListResponse> {
    const response = await apiClient.get<RiskAlertListResponse>('/risk-alerts', {
      params: {
        include_resolved: includeResolved,
        level,
        limit,
        offset,
      },
    });
    return response.data;
  },

  /**
   * 获取风险预警统计
   */
  async getStats(): Promise<{
    total_alerts: number;
    unread_count: number;
    resolved_count: number;
    by_level: Record<string, number>;
    by_type: Record<string, number>;
    recent_alerts: RiskAlert[];
  }> {
    const response = await apiClient.get('/risk-alerts/stats');
    return response.data;
  },

  /**
   * 手动触发风险检查
   */
  async checkRisks(): Promise<{ message: string; alerts: RiskAlert[] }> {
    const response = await apiClient.post('/risk-alerts/check');
    return response.data;
  },

  /**
   * 标记预警为已读
   */
  async markAsRead(alertId: number): Promise<RiskAlert> {
    const response = await apiClient.put<RiskAlert>(`/risk-alerts/${alertId}/read`);
    return response.data;
  },

  /**
   * 标记所有预警为已读
   */
  async markAllAsRead(): Promise<{ message: string }> {
    const response = await apiClient.put('/risk-alerts/read-all');
    return response.data;
  },

  /**
   * 解决风险预警
   */
  async resolveAlert(alertId: number, resolutionNote?: string): Promise<RiskAlert> {
    const response = await apiClient.put<RiskAlert>(`/risk-alerts/${alertId}/resolve`, {
      resolution_note: resolutionNote,
    });
    return response.data;
  },
};

/**
 * 用户偏好配置服务
 */
export const preferenceService = {
  /**
   * 获取用户偏好配置
   */
  async getPreference(): Promise<UserPreference> {
    const response = await apiClient.get<UserPreference>('/preferences');
    return response.data;
  },

  /**
   * 更新用户偏好配置
   */
  async updatePreference(data: Partial<UserPreference>): Promise<UserPreference> {
    const response = await apiClient.put<UserPreference>('/preferences', data);
    return response.data;
  },

  /**
   * 更新周提醒设置
   */
  async updateWeeklyReminder(
    enabled?: boolean,
    day?: number,
    time?: string
  ): Promise<UserPreference> {
    const params = new URLSearchParams();
    if (enabled !== undefined) params.append('enabled', String(enabled));
    if (day !== undefined) params.append('day', String(day));
    if (time) params.append('time', time);
    
    const response = await apiClient.put<UserPreference>(
      `/preferences/weekly-reminder?${params.toString()}`
    );
    return response.data;
  },

  /**
   * 更新月度报告设置
   */
  async updateMonthlyReport(
    enabled?: boolean,
    day?: number,
    time?: string
  ): Promise<UserPreference> {
    const params = new URLSearchParams();
    if (enabled !== undefined) params.append('enabled', String(enabled));
    if (day !== undefined) params.append('day', String(day));
    if (time) params.append('time', time);
    
    const response = await apiClient.put<UserPreference>(
      `/preferences/monthly-report?${params.toString()}`
    );
    return response.data;
  },

  /**
   * 更新风险预警设置
   */
  async updateRiskAlert(enabled?: boolean, threshold?: string): Promise<UserPreference> {
    const params = new URLSearchParams();
    if (enabled !== undefined) params.append('enabled', String(enabled));
    if (threshold) params.append('threshold', threshold);
    
    const response = await apiClient.put<UserPreference>(
      `/preferences/risk-alert?${params.toString()}`
    );
    return response.data;
  },

  /**
   * 更新通知渠道
   */
  async updateNotificationChannels(channels: string[]): Promise<UserPreference> {
    const response = await apiClient.put<UserPreference>(
      `/preferences/notification-channels`,
      channels
    );
    return response.data;
  },

  /**
   * 重置为默认设置
   */
  async resetToDefault(): Promise<UserPreference> {
    const response = await apiClient.post<UserPreference>('/preferences/reset');
    return response.data;
  },
};

export default cashFlowService;
