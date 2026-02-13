/**
 * 报表状态管理
 */
import { create } from 'zustand';
import type { ReportData, ReportFilters, CategoryAnalysis, ReportType, ExportFormat } from '@/types/report';
import reportService from '@/services/reportService';

interface ReportState {
  dailyReport: ReportData | null;
  weeklyReport: ReportData | null;
  monthlyReport: ReportData | null;
  customReport: ReportData | null;
  categoryAnalysis: CategoryAnalysis | null;
  isLoading: boolean;
  error: string | null;

  getDailyReport: (date?: string) => Promise<void>;
  getWeeklyReport: (startDate?: string, endDate?: string) => Promise<void>;
  getMonthlyReport: (year?: number, month?: number) => Promise<void>;
  getCustomReport: (filters: ReportFilters) => Promise<void>;
  getCategoryAnalysis: (startDate: string, endDate: string, type?: string) => Promise<void>;
  exportReport: (reportData: ReportData, format: ExportFormat, reportType: ReportType) => Promise<void>;
  clearError: () => void;
}

const useReportStore = create<ReportState>((set) => ({
  dailyReport: null,
  weeklyReport: null,
  monthlyReport: null,
  customReport: null,
  categoryAnalysis: null,
  isLoading: false,
  error: null,

  getDailyReport: async (date?: string) => {
    set({ isLoading: true, error: null });
    try {
      const data = await reportService.getDailyReport(date);
      set({ dailyReport: data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取每日报表失败',
        isLoading: false,
      });
    }
  },

  getWeeklyReport: async (startDate?: string, endDate?: string) => {
    set({ isLoading: true, error: null });
    try {
      const data = await reportService.getWeeklyReport(startDate, endDate);
      set({ weeklyReport: data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取每周报表失败',
        isLoading: false,
      });
    }
  },

  getMonthlyReport: async (year?: number, month?: number) => {
    set({ isLoading: true, error: null });
    try {
      const data = await reportService.getMonthlyReport(year, month);
      set({ monthlyReport: data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取每月报表失败',
        isLoading: false,
      });
    }
  },

  getCustomReport: async (filters: ReportFilters) => {
    set({ isLoading: true, error: null });
    try {
      const data = await reportService.getCustomReport(filters);
      set({ customReport: data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取自定义报表失败',
        isLoading: false,
      });
    }
  },

  getCategoryAnalysis: async (startDate: string, endDate: string, type: string = 'all') => {
    set({ isLoading: true, error: null });
    try {
      const data = await reportService.getCategoryAnalysis(startDate, endDate, type);
      set({ categoryAnalysis: data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '获取分类分析失败',
        isLoading: false,
      });
    }
  },

  exportReport: async (reportData: ReportData, format: ExportFormat, reportType: ReportType) => {
    set({ isLoading: true, error: null });
    try {
      let blob: Blob;
      let filename: string;

      if (format === 'excel') {
        blob = await reportService.exportExcel(reportData, reportType);
        filename = `报表_${reportType}.xlsx`;
      } else {
        blob = await reportService.exportPdf(reportData, reportType);
        filename = `报表_${reportType}.pdf`;
      }

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      set({ isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '导出报表失败',
        isLoading: false,
      });
    }
  },

  clearError: () => set({ error: null }),
}));

export default useReportStore;
