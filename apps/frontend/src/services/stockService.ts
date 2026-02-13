/**
 * 库存API服务
 */
import apiClient from './apiClient';
import type {
  Ingredient,
  StockRecord,
  StockWarning,
  StockSummary,
  IngredientCreateParams,
  IngredientUpdateParams,
  StockRecordParams,
  IngredientListResponse,
  StockRecordListResponse,
} from '@/types/stock';

/**
 * 库存服务对象
 */
export const stockService = {
  /**
   * 创建食材
   */
  createIngredient: async (data: IngredientCreateParams): Promise<Ingredient> => {
    const response = await apiClient.post<Ingredient>('/stock/ingredients', data);
    return response.data;
  },

  /**
   * 获取食材列表
   */
  listIngredients: async (
    name?: string,
    page = 1,
    pageSize = 100
  ): Promise<IngredientListResponse> => {
    const params = new URLSearchParams();
    if (name) params.append('name', name);
    params.append('page', String(page));
    params.append('page_size', String(pageSize));
    const response = await apiClient.get<IngredientListResponse>(
      `/stock/ingredients?${params.toString()}`
    );
    return response.data;
  },

  /**
   * 获取食材详情
   */
  getIngredient: async (ingredientId: number): Promise<Ingredient> => {
    const response = await apiClient.get<Ingredient>(`/stock/ingredients/${ingredientId}`);
    return response.data;
  },

  /**
   * 更新食材
   */
  updateIngredient: async (
    ingredientId: number,
    data: IngredientUpdateParams
  ): Promise<Ingredient> => {
    const response = await apiClient.put<Ingredient>(
      `/stock/ingredients/${ingredientId}`,
      data
    );
    return response.data;
  },

  /**
   * 删除食材
   */
  deleteIngredient: async (ingredientId: number): Promise<void> => {
    await apiClient.delete(`/stock/ingredients/${ingredientId}`);
  },

  /**
   * 记录库存入库
   */
  recordStockIn: async (data: StockRecordParams): Promise<StockRecord> => {
    const response = await apiClient.post<StockRecord>('/stock/records/in', data);
    return response.data;
  },

  /**
   * 记录库存出库
   */
  recordStockOut: async (data: StockRecordParams): Promise<StockRecord> => {
    const response = await apiClient.post<StockRecord>('/stock/records/out', data);
    return response.data;
  },

  /**
   * 获取库存记录列表
   */
  listStockRecords: async (
    ingredientId?: number,
    type?: string,
    page = 1,
    pageSize = 20
  ): Promise<StockRecordListResponse> => {
    const params = new URLSearchParams();
    if (ingredientId) params.append('ingredient_id', String(ingredientId));
    if (type) params.append('type', type);
    params.append('page', String(page));
    params.append('page_size', String(pageSize));
    const response = await apiClient.get<StockRecordListResponse>(
      `/stock/records?${params.toString()}`
    );
    return response.data;
  },

  /**
   * 获取库存预警列表
   */
  getStockWarnings: async (): Promise<StockWarning[]> => {
    const response = await apiClient.get<StockWarning[]>('/stock/warnings');
    return response.data;
  },

  /**
   * 获取库存统计
   */
  getStockSummary: async (): Promise<StockSummary> => {
    const response = await apiClient.get<StockSummary>('/stock/summary');
    return response.data;
  },
};
