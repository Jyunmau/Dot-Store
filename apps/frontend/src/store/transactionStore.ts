/**
 * 收支记录状态管理
 */
import { create } from 'zustand';
import type {
  Transaction,
  TransactionCategory,
  TransactionCreateParams,
  TransactionUpdateParams,
  TransactionCategoryCreateParams,
  TransactionCategoryUpdateParams,
  TransactionFilters,
  TransactionListResponse,
  TransactionSummary,
} from '@/types/transaction';
import { transactionService } from '@/services/transactionService';

interface TransactionState {
  transactions: Transaction[];
  currentTransaction: Transaction | null;
  categories: TransactionCategory[];
  summary: TransactionSummary | null;
  total: number;
  page: number;
  pageSize: number;
  isLoading: boolean;
  error: string | null;

  createTransaction: (data: TransactionCreateParams) => Promise<Transaction>;
  listTransactions: (filters?: TransactionFilters) => Promise<void>;
  getTransaction: (transactionId: number) => Promise<void>;
  updateTransaction: (transactionId: number, data: TransactionUpdateParams) => Promise<Transaction>;
  deleteTransaction: (transactionId: number) => Promise<void>;
  getTransactionSummary: (startDate?: string, endDate?: string) => Promise<void>;
  createCategory: (data: TransactionCategoryCreateParams) => Promise<TransactionCategory>;
  listCategories: (type?: 'income' | 'expense') => Promise<void>;
  updateCategory: (categoryId: number, data: TransactionCategoryUpdateParams) => Promise<TransactionCategory>;
  deleteCategory: (categoryId: number) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  transactions: [],
  currentTransaction: null,
  categories: [],
  summary: null,
  total: 0,
  page: 1,
  pageSize: 10,
  isLoading: false,
  error: null,
};

export const useTransactionStore = create<TransactionState>((set) => ({
  ...initialState,

  createTransaction: async (data: TransactionCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const transaction = await transactionService.createTransaction(data);
      set((state) => ({
        transactions: [transaction, ...state.transactions],
        total: state.total + 1,
        isLoading: false,
      }));
      return transaction;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '创建收支记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  listTransactions: async (filters?: TransactionFilters) => {
    set({ isLoading: true, error: null });
    try {
      const response: TransactionListResponse = await transactionService.listTransactions(filters);
      set({
        transactions: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取收支记录列表失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getTransaction: async (transactionId: number) => {
    set({ isLoading: true, error: null });
    try {
      const transaction = await transactionService.getTransaction(transactionId);
      set({ currentTransaction: transaction, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取收支记录详情失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updateTransaction: async (transactionId: number, data: TransactionUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const transaction = await transactionService.updateTransaction(transactionId, data);
      set((state) => ({
        transactions: state.transactions.map((t) => (t.id === transactionId ? transaction : t)),
        currentTransaction: state.currentTransaction?.id === transactionId ? transaction : state.currentTransaction,
        isLoading: false,
      }));
      return transaction;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '更新收支记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  deleteTransaction: async (transactionId: number) => {
    set({ isLoading: true, error: null });
    try {
      await transactionService.deleteTransaction(transactionId);
      set((state) => ({
        transactions: state.transactions.filter((t) => t.id !== transactionId),
        total: state.total - 1,
        isLoading: false,
      }));
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '删除收支记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getTransactionSummary: async (startDate?: string, endDate?: string) => {
    set({ isLoading: true, error: null });
    try {
      const summary = await transactionService.getTransactionSummary(startDate, endDate);
      set({ summary, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取收支汇总失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  createCategory: async (data: TransactionCategoryCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const category = await transactionService.createCategory(data);
      set((state) => ({
        categories: [...state.categories, category],
        isLoading: false,
      }));
      return category;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '创建分类失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  listCategories: async (type?: 'income' | 'expense') => {
    set({ isLoading: true, error: null });
    try {
      const categories = await transactionService.listCategories(type);
      set({ categories, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取分类列表失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updateCategory: async (categoryId: number, data: TransactionCategoryUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const category = await transactionService.updateCategory(categoryId, data);
      set((state) => ({
        categories: state.categories.map((c) => (c.id === categoryId ? category : c)),
        isLoading: false,
      }));
      return category;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '更新分类失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  deleteCategory: async (categoryId: number) => {
    set({ isLoading: true, error: null });
    try {
      await transactionService.deleteCategory(categoryId);
      set((state) => ({
        categories: state.categories.filter((c) => c.id !== categoryId),
        isLoading: false,
      }));
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '删除分类失败';
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
