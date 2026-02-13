/**
 * 订单状态管理
 */
import { create } from 'zustand';
import type {
  Order,
  OrderCategory,
  OrderCreateParams,
  OrderUpdateParams,
  OrderCategoryCreateParams,
  OrderCategoryUpdateParams,
  OrderFilters,
  OrderListResponse,
} from '@/types/order';
import { orderService } from '@/services/orderService';

interface OrderState {
  orders: Order[];
  currentOrder: Order | null;
  recycleOrders: Order[];
  categories: OrderCategory[];
  orderTypes: string[];
  orderTags: string[];
  total: number;
  page: number;
  pageSize: number;
  isLoading: boolean;
  error: string | null;

  createOrder: (data: OrderCreateParams) => Promise<Order>;
  listOrders: (filters?: OrderFilters) => Promise<void>;
  getOrder: (orderId: number) => Promise<void>;
  updateOrder: (orderId: number, data: OrderUpdateParams) => Promise<Order>;
  deleteOrder: (orderId: number) => Promise<void>;
  restoreOrder: (orderId: number) => Promise<void>;
  getRecycleOrders: (page?: number, pageSize?: number) => Promise<void>;
  getOrderTypes: () => Promise<void>;
  getOrderTags: () => Promise<void>;
  createCategory: (data: OrderCategoryCreateParams) => Promise<OrderCategory>;
  listCategories: () => Promise<void>;
  updateCategory: (categoryId: number, data: OrderCategoryUpdateParams) => Promise<OrderCategory>;
  deleteCategory: (categoryId: number) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  orders: [],
  currentOrder: null,
  recycleOrders: [],
  categories: [],
  orderTypes: [],
  orderTags: [],
  total: 0,
  page: 1,
  pageSize: 10,
  isLoading: false,
  error: null,
};

export const useOrderStore = create<OrderState>((set, get) => ({
  ...initialState,

  createOrder: async (data: OrderCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const order = await orderService.createOrder(data);
      set((state) => ({
        orders: [order, ...state.orders],
        total: state.total + 1,
        isLoading: false,
      }));
      return order;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '创建订单失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  listOrders: async (filters?: OrderFilters) => {
    set({ isLoading: true, error: null });
    try {
      const response: OrderListResponse = await orderService.listOrders(filters);
      set({
        orders: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取订单列表失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getOrder: async (orderId: number) => {
    set({ isLoading: true, error: null });
    try {
      const order = await orderService.getOrder(orderId);
      set({ currentOrder: order, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取订单详情失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updateOrder: async (orderId: number, data: OrderUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const order = await orderService.updateOrder(orderId, data);
      set((state) => ({
        orders: state.orders.map((o) => (o.id === orderId ? order : o)),
        currentOrder: state.currentOrder?.id === orderId ? order : state.currentOrder,
        isLoading: false,
      }));
      return order;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '更新订单失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  deleteOrder: async (orderId: number) => {
    set({ isLoading: true, error: null });
    try {
      await orderService.deleteOrder(orderId);
      set((state) => ({
        orders: state.orders.filter((o) => o.id !== orderId),
        total: state.total - 1,
        isLoading: false,
      }));
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '删除订单失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  restoreOrder: async (orderId: number) => {
    set({ isLoading: true, error: null });
    try {
      await orderService.restoreOrder(orderId);
      set((state) => ({
        recycleOrders: state.recycleOrders.filter((o) => o.id !== orderId),
        isLoading: false,
      }));
      await get().listOrders();
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '恢复订单失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getRecycleOrders: async (page = 1, pageSize = 10) => {
    set({ isLoading: true, error: null });
    try {
      const response = await orderService.getRecycleOrders(page, pageSize);
      set({
        recycleOrders: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取回收站订单失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getOrderTypes: async () => {
    try {
      const types = await orderService.getOrderTypes();
      set({ orderTypes: types });
    } catch (error: unknown) {
      console.error('获取订单类型失败:', error);
    }
  },

  getOrderTags: async () => {
    try {
      const tags = await orderService.getOrderTags();
      set({ orderTags: tags });
    } catch (error: unknown) {
      console.error('获取订单标签失败:', error);
    }
  },

  createCategory: async (data: OrderCategoryCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const category = await orderService.createCategory(data);
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

  listCategories: async () => {
    set({ isLoading: true, error: null });
    try {
      const categories = await orderService.listCategories();
      set({ categories, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取分类列表失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updateCategory: async (categoryId: number, data: OrderCategoryUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const category = await orderService.updateCategory(categoryId, data);
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
      await orderService.deleteCategory(categoryId);
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
