/**
 * 订单API服务
 */
import apiClient from './apiClient';
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

/**
 * 订单服务对象
 */
export const orderService = {
  /**
   * 创建订单
   */
  createOrder: async (data: OrderCreateParams): Promise<Order> => {
    const response = await apiClient.post<Order>('/orders', data);
    return response.data;
  },

  /**
   * 获取订单列表
   */
  listOrders: async (filters?: OrderFilters): Promise<OrderListResponse> => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.order_type) params.append('order_type', filters.order_type);
      if (filters.category_id) params.append('category_id', String(filters.category_id));
      if (filters.status) params.append('status', filters.status);
      if (filters.tags) params.append('tags', filters.tags);
      if (filters.page) params.append('page', String(filters.page));
      if (filters.page_size) params.append('page_size', String(filters.page_size));
    }
    const response = await apiClient.get<OrderListResponse>(`/orders?${params.toString()}`);
    return response.data;
  },

  /**
   * 获取订单详情
   */
  getOrder: async (orderId: number): Promise<Order> => {
    const response = await apiClient.get<Order>(`/orders/${orderId}`);
    return response.data;
  },

  /**
   * 更新订单
   */
  updateOrder: async (orderId: number, data: OrderUpdateParams): Promise<Order> => {
    const response = await apiClient.put<Order>(`/orders/${orderId}`, data);
    return response.data;
  },

  /**
   * 删除订单
   */
  deleteOrder: async (orderId: number): Promise<void> => {
    await apiClient.delete(`/orders/${orderId}`);
  },

  /**
   * 恢复订单
   */
  restoreOrder: async (orderId: number): Promise<Order> => {
    const response = await apiClient.post<Order>(`/orders/${orderId}/restore`);
    return response.data;
  },

  /**
   * 获取回收站订单
   */
  getRecycleOrders: async (page = 1, pageSize = 10): Promise<OrderListResponse> => {
    const response = await apiClient.get<OrderListResponse>(
      `/orders/recycle?page=${page}&page_size=${pageSize}`
    );
    return response.data;
  },

  /**
   * 获取订单类型列表
   */
  getOrderTypes: async (): Promise<string[]> => {
    const response = await apiClient.get<{ types: string[] }>('/orders/types');
    return response.data.types;
  },

  /**
   * 获取订单标签列表
   */
  getOrderTags: async (): Promise<string[]> => {
    const response = await apiClient.get<{ tags: string[] }>('/orders/tags');
    return response.data.tags;
  },

  /**
   * 创建订单分类
   */
  createCategory: async (data: OrderCategoryCreateParams): Promise<OrderCategory> => {
    const response = await apiClient.post<OrderCategory>('/orders/categories', data);
    return response.data;
  },

  /**
   * 获取订单分类列表
   */
  listCategories: async (): Promise<OrderCategory[]> => {
    const response = await apiClient.get<OrderCategory[]>('/orders/categories');
    return response.data;
  },

  /**
   * 获取订单分类详情
   */
  getCategory: async (categoryId: number): Promise<OrderCategory> => {
    const response = await apiClient.get<OrderCategory>(`/orders/categories/${categoryId}`);
    return response.data;
  },

  /**
   * 更新订单分类
   */
  updateCategory: async (
    categoryId: number,
    data: OrderCategoryUpdateParams
  ): Promise<OrderCategory> => {
    const response = await apiClient.put<OrderCategory>(
      `/orders/categories/${categoryId}`,
      data
    );
    return response.data;
  },

  /**
   * 删除订单分类
   */
  deleteCategory: async (categoryId: number): Promise<void> => {
    await apiClient.delete(`/orders/categories/${categoryId}`);
  },

  /**
   * 获取分类使用情况
   */
  getCategoryUsage: async (
    categoryId: number
  ): Promise<{ category_id: number; category_name: string; order_count: number }> => {
    const response = await apiClient.get(`/orders/categories/${categoryId}/usage`);
    return response.data;
  },
};
