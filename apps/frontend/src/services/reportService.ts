/**
 * 报表服务
 */
import apiClient from './apiClient';
import type { ReportData, ReportFilters, CategoryAnalysis, ExportRequest } from '@/types/report';

/**
 * 报表API服务
 */
export const reportService = {
  /**
   * 获取每日报表
   */
  getDailyReport: async (date?: string): Promise<ReportData> => {
    const params = date ? { date } : {};
    const response = await apiClient.get('/reports/daily', { params });
    return response.data.data;
  },

  /**
   * 获取每周报表
   */
  getWeeklyReport: async (startDate?: string, endDate?: string): Promise<ReportData> => {
    const params: Record<string, string> = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    const response = await apiClient.get('/reports/weekly', { params });
    return response.data.data;
  },

  /**
   * 获取每月报表
   */
  getMonthlyReport: async (year?: number, month?: number): Promise<ReportData> => {
    const params: Record<string, number> = {};
    if (year) params.year = year;
    if (month) params.month = month;
    const response = await apiClient.get('/reports/monthly', { params });
    return response.data.data;
  },

  /**
   * 获取自定义报表
   */
  getCustomReport: async (filters: ReportFilters): Promise<ReportData> => {
    const response = await apiClient.post('/reports/custom', filters);
    return response.data.data;
  },

  /**
   * 获取分类分析
   */
  getCategoryAnalysis: async (startDate: string, endDate: string, type: string = 'all'): Promise<CategoryAnalysis> => {
    const response = await apiClient.get('/reports/category-analysis', {
      params: {
        start_date: startDate,
        end_date: endDate,
        type,
      },
    });
    return response.data.data;
  },

  /**
   * 导出报表为Excel
   */
  exportExcel: async (reportData: ReportData, reportType: string): Promise<Blob> => {
    const response = await apiClient.post('/reports/export/excel', {
      report_data: reportData,
      report_type: reportType,
    } as ExportRequest, {
      responseType: 'blob',
    });
    return response.data;
  },

  /**
   * 导出报表为PDF
   */
  exportPdf: async (reportData: ReportData, reportType: string): Promise<Blob> => {
    const response = await apiClient.post('/reports/export/pdf', {
      report_data: reportData,
      report_type: reportType,
    } as ExportRequest, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default reportService;
