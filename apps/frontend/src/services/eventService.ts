/**
 * Dot-Store V2.2 事件日志API服务
 */
import apiClient from './apiClient';
import type { EventListResponse, EventQueryParams, BusinessEvent } from '../types/event';

export const eventService = {
  /**
   * 获取事件列表
   */
  getEvents: async (params?: EventQueryParams): Promise<EventListResponse> => {
    const response = await apiClient.get('/events', { params });
    return response.data;
  },

  /**
   * 获取事件详情
   */
  getEvent: async (eventId: number): Promise<BusinessEvent> => {
    const response = await apiClient.get(`/events/${eventId}`);
    return response.data;
  },

  /**
   * 获取实体相关事件
   */
  getEntityEvents: async (entityType: string, entityId: number): Promise<BusinessEvent[]> => {
    const response = await apiClient.get(`/events/entity/${entityType}/${entityId}`);
    return response.data;
  },
};

export default eventService;
