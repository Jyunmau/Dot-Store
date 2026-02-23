/**
 * Dot-Store V2.2 现金流状态管理
 */
import { create } from 'zustand';
import type {
  SafetyIndex,
  DashboardData,
  CashFlowForecastListResponse,
  RiskAlertListResponse,
  IncomeStructureResponse,
  ExpenseStructureResponse,
  BreakEvenAnalysis,
  MonthlyReport,
  IncomeVolatility,
  UserPreference,
} from '@/types/cashFlow';
import cashFlowService, { riskAlertService, preferenceService } from '@/services/cashFlowService';

interface CashFlowState {
  safetyIndex: SafetyIndex | null;
  dashboardData: DashboardData | null;
  forecastData: CashFlowForecastListResponse | null;
  riskAlerts: RiskAlertListResponse | null;
  incomeStructure: IncomeStructureResponse | null;
  expenseStructure: ExpenseStructureResponse | null;
  breakEvenAnalysis: BreakEvenAnalysis | null;
  monthlyReport: MonthlyReport | null;
  incomeVolatility: IncomeVolatility | null;
  userPreference: UserPreference | null;
  loading: boolean;
  error: string | null;

  fetchSafetyIndex: () => Promise<void>;
  fetchDashboard: () => Promise<void>;
  fetchForecast: (days?: number) => Promise<void>;
  fetchRiskAlerts: (includeResolved?: boolean, level?: string) => Promise<void>;
  fetchIncomeStructure: (periodStart: string, periodEnd: string) => Promise<void>;
  fetchExpenseStructure: (periodStart: string, periodEnd: string) => Promise<void>;
  fetchBreakEvenAnalysis: () => Promise<void>;
  fetchMonthlyReport: (year: number, month: number) => Promise<void>;
  fetchIncomeVolatility: () => Promise<void>;
  fetchUserPreference: () => Promise<void>;
  updateUserPreference: (data: Partial<UserPreference>) => Promise<void>;
  resolveAlert: (alertId: number, resolutionNote?: string) => Promise<void>;
  markAlertAsRead: (alertId: number) => Promise<void>;
  markAllAlertsAsRead: () => Promise<void>;
  checkRisks: () => Promise<void>;
  clearError: () => void;
}

/**
 * 现金流状态管理Store
 */
export const useCashFlowStore = create<CashFlowState>((set, get) => ({
  safetyIndex: null,
  dashboardData: null,
  forecastData: null,
  riskAlerts: null,
  incomeStructure: null,
  expenseStructure: null,
  breakEvenAnalysis: null,
  monthlyReport: null,
  incomeVolatility: null,
  userPreference: null,
  loading: false,
  error: null,

  /**
   * 获取安全指数
   */
  fetchSafetyIndex: async () => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getSafetyIndex();
      set({ safetyIndex: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取安全指数失败',
        loading: false,
      });
    }
  },

  /**
   * 获取仪表盘数据
   */
  fetchDashboard: async () => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getDashboard();
      set({
        dashboardData: data,
        safetyIndex: data.safety_index,
        loading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取仪表盘数据失败',
        loading: false,
      });
    }
  },

  /**
   * 获取现金流预测
   */
  fetchForecast: async (days: number = 30) => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getForecast(days);
      set({ forecastData: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取现金流预测失败',
        loading: false,
      });
    }
  },

  /**
   * 获取风险预警列表
   */
  fetchRiskAlerts: async (includeResolved: boolean = false, level?: string) => {
    try {
      set({ loading: true, error: null });
      const data = await riskAlertService.getAlerts(includeResolved, level);
      set({ riskAlerts: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取风险预警失败',
        loading: false,
      });
    }
  },

  /**
   * 获取收入结构
   */
  fetchIncomeStructure: async (periodStart: string, periodEnd: string) => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getIncomeStructure(periodStart, periodEnd);
      set({ incomeStructure: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取收入结构失败',
        loading: false,
      });
    }
  },

  /**
   * 获取支出结构
   */
  fetchExpenseStructure: async (periodStart: string, periodEnd: string) => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getExpenseStructure(periodStart, periodEnd);
      set({ expenseStructure: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取支出结构失败',
        loading: false,
      });
    }
  },

  /**
   * 获取盈亏平衡分析
   */
  fetchBreakEvenAnalysis: async () => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getBreakEvenAnalysis();
      set({ breakEvenAnalysis: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取盈亏平衡分析失败',
        loading: false,
      });
    }
  },

  /**
   * 获取月度健康报告
   */
  fetchMonthlyReport: async (year: number, month: number) => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getMonthlyReport(year, month);
      set({ monthlyReport: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取月度报告失败',
        loading: false,
      });
    }
  },

  /**
   * 获取收入波动归因
   */
  fetchIncomeVolatility: async () => {
    try {
      set({ loading: true, error: null });
      const data = await cashFlowService.getIncomeVolatility();
      set({ incomeVolatility: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取收入波动分析失败',
        loading: false,
      });
    }
  },

  /**
   * 获取用户偏好配置
   */
  fetchUserPreference: async () => {
    try {
      set({ loading: true, error: null });
      const data = await preferenceService.getPreference();
      set({ userPreference: data, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取用户偏好失败',
        loading: false,
      });
    }
  },

  /**
   * 更新用户偏好配置
   */
  updateUserPreference: async (data: Partial<UserPreference>) => {
    try {
      set({ loading: true, error: null });
      const updated = await preferenceService.updatePreference(data);
      set({ userPreference: updated, loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '更新用户偏好失败',
        loading: false,
      });
    }
  },

  /**
   * 解决风险预警
   */
  resolveAlert: async (alertId: number, resolutionNote?: string) => {
    try {
      await riskAlertService.resolveAlert(alertId, resolutionNote);
      const { riskAlerts } = get();
      if (riskAlerts) {
        set({
          riskAlerts: {
            ...riskAlerts,
            items: riskAlerts.items.map((a) =>
              a.id === alertId ? { ...a, is_resolved: true } : a
            ),
          },
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '解决预警失败',
      });
    }
  },

  /**
   * 标记预警为已读
   */
  markAlertAsRead: async (alertId: number) => {
    try {
      await riskAlertService.markAsRead(alertId);
      const { riskAlerts } = get();
      if (riskAlerts) {
        set({
          riskAlerts: {
            ...riskAlerts,
            items: riskAlerts.items.map((a) =>
              a.id === alertId ? { ...a, is_read: true } : a
            ),
            unread_count: Math.max(0, riskAlerts.unread_count - 1),
          },
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '标记已读失败',
      });
    }
  },

  /**
   * 标记所有预警为已读
   */
  markAllAlertsAsRead: async () => {
    try {
      await riskAlertService.markAllAsRead();
      const { riskAlerts } = get();
      if (riskAlerts) {
        set({
          riskAlerts: {
            ...riskAlerts,
            items: riskAlerts.items.map((a) => ({ ...a, is_read: true })),
            unread_count: 0,
          },
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '标记全部已读失败',
      });
    }
  },

  /**
   * 手动触发风险检查
   */
  checkRisks: async () => {
    try {
      set({ loading: true, error: null });
      const result = await riskAlertService.checkRisks();
      const { fetchRiskAlerts } = get();
      await fetchRiskAlerts();
      set({ loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '风险检查失败',
        loading: false,
      });
    }
  },

  /**
   * 清除错误
   */
  clearError: () => set({ error: null }),
}));

export default useCashFlowStore;
