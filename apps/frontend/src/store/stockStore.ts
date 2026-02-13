/**
 * 库存状态管理
 */
import { create } from 'zustand';
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
import { stockService } from '@/services/stockService';

interface StockState {
  ingredients: Ingredient[];
  stockRecords: StockRecord[];
  stockWarnings: StockWarning[];
  stockSummary: StockSummary | null;
  total: number;
  page: number;
  pageSize: number;
  recordsTotal: number;
  recordsPage: number;
  recordsPageSize: number;
  isLoading: boolean;
  error: string | null;

  createIngredient: (data: IngredientCreateParams) => Promise<Ingredient>;
  listIngredients: (name?: string, page?: number, pageSize?: number) => Promise<void>;
  getIngredient: (ingredientId: number) => Promise<Ingredient>;
  updateIngredient: (ingredientId: number, data: IngredientUpdateParams) => Promise<Ingredient>;
  deleteIngredient: (ingredientId: number) => Promise<void>;
  recordStockIn: (data: StockRecordParams) => Promise<StockRecord>;
  recordStockOut: (data: StockRecordParams) => Promise<StockRecord>;
  listStockRecords: (
    ingredientId?: number,
    type?: string,
    page?: number,
    pageSize?: number
  ) => Promise<void>;
  getStockWarnings: () => Promise<void>;
  getStockSummary: () => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  ingredients: [],
  stockRecords: [],
  stockWarnings: [],
  stockSummary: null,
  total: 0,
  page: 1,
  pageSize: 100,
  recordsTotal: 0,
  recordsPage: 1,
  recordsPageSize: 20,
  isLoading: false,
  error: null,
};

export const useStockStore = create<StockState>((set) => ({
  ...initialState,

  createIngredient: async (data: IngredientCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const ingredient = await stockService.createIngredient(data);
      set((state) => ({
        ingredients: [...state.ingredients, ingredient],
        total: state.total + 1,
        isLoading: false,
      }));
      return ingredient;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '创建食材失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  listIngredients: async (name?: string, page = 1, pageSize = 100) => {
    set({ isLoading: true, error: null });
    try {
      const response: IngredientListResponse = await stockService.listIngredients(
        name,
        page,
        pageSize
      );
      set({
        ingredients: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取食材列表失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getIngredient: async (ingredientId: number) => {
    set({ isLoading: true, error: null });
    try {
      const ingredient = await stockService.getIngredient(ingredientId);
      set({ isLoading: false });
      return ingredient;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取食材详情失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updateIngredient: async (ingredientId: number, data: IngredientUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const ingredient = await stockService.updateIngredient(ingredientId, data);
      set((state) => ({
        ingredients: state.ingredients.map((ing) =>
          ing.id === ingredientId ? ingredient : ing
        ),
        isLoading: false,
      }));
      return ingredient;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '更新食材失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  deleteIngredient: async (ingredientId: number) => {
    set({ isLoading: true, error: null });
    try {
      await stockService.deleteIngredient(ingredientId);
      set((state) => ({
        ingredients: state.ingredients.filter((ing) => ing.id !== ingredientId),
        total: state.total - 1,
        isLoading: false,
      }));
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '删除食材失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  recordStockIn: async (data: StockRecordParams) => {
    set({ isLoading: true, error: null });
    try {
      const record = await stockService.recordStockIn(data);
      set((state) => ({
        stockRecords: [record, ...state.stockRecords],
        recordsTotal: state.recordsTotal + 1,
        ingredients: state.ingredients.map((ing) =>
          ing.id === data.ingredient_id
            ? {
                ...ing,
                current_stock: String(
                  Number(ing.current_stock) + Number(data.quantity)
                ),
              }
            : ing
        ),
        isLoading: false,
      }));
      return record;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '入库记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  recordStockOut: async (data: StockRecordParams) => {
    set({ isLoading: true, error: null });
    try {
      const record = await stockService.recordStockOut(data);
      set((state) => ({
        stockRecords: [record, ...state.stockRecords],
        recordsTotal: state.recordsTotal + 1,
        ingredients: state.ingredients.map((ing) =>
          ing.id === data.ingredient_id
            ? {
                ...ing,
                current_stock: String(
                  Number(ing.current_stock) - Number(data.quantity)
                ),
              }
            : ing
        ),
        isLoading: false,
      }));
      return record;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '出库记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  listStockRecords: async (
    ingredientId?: number,
    type?: string,
    page = 1,
    pageSize = 20
  ) => {
    set({ isLoading: true, error: null });
    try {
      const response: StockRecordListResponse = await stockService.listStockRecords(
        ingredientId,
        type,
        page,
        pageSize
      );
      set({
        stockRecords: response.items,
        recordsTotal: response.total,
        recordsPage: response.page,
        recordsPageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取库存记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getStockWarnings: async () => {
    set({ isLoading: true, error: null });
    try {
      const warnings = await stockService.getStockWarnings();
      set({ stockWarnings: warnings, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取库存预警失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getStockSummary: async () => {
    set({ isLoading: true, error: null });
    try {
      const summary = await stockService.getStockSummary();
      set({ stockSummary: summary, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取库存统计失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },

  reset: () => {
    set(initialState);
  },
}));
