/**
 * 会员API服务
 */
import apiClient from './apiClient';
import type {
  Member,
  PointsRecord,
  PointsExchange,
  MemberCreateParams,
  MemberUpdateParams,
  MemberListResponse,
  PointsAddParams,
  PointsSubtractParams,
  PointsRecordListResponse,
  PointsExchangeParams,
  PointsExchangeListResponse,
} from '@/types/member';

/**
 * 会员服务对象
 */
export const memberService = {
  /**
   * 创建会员
   */
  createMember: async (data: MemberCreateParams): Promise<Member> => {
    const response = await apiClient.post<Member>('/members', data);
    return response.data;
  },

  /**
   * 获取会员列表
   */
  listMembers: async (params?: {
    page?: number;
    page_size?: number;
    level?: string;
    keyword?: string;
  }): Promise<MemberListResponse> => {
    const searchParams = new URLSearchParams();
    if (params) {
      if (params.page) searchParams.append('page', String(params.page));
      if (params.page_size) searchParams.append('page_size', String(params.page_size));
      if (params.level) searchParams.append('level', params.level);
      if (params.keyword) searchParams.append('keyword', params.keyword);
    }
    const response = await apiClient.get<MemberListResponse>(`/members?${searchParams.toString()}`);
    return response.data;
  },

  /**
   * 获取会员详情
   */
  getMember: async (memberId: number): Promise<Member> => {
    const response = await apiClient.get<Member>(`/members/${memberId}`);
    return response.data;
  },

  /**
   * 更新会员
   */
  updateMember: async (memberId: number, data: MemberUpdateParams): Promise<Member> => {
    const response = await apiClient.put<Member>(`/members/${memberId}`, data);
    return response.data;
  },

  /**
   * 删除会员
   */
  deleteMember: async (memberId: number): Promise<void> => {
    await apiClient.delete(`/members/${memberId}`);
  },

  /**
   * 增加积分
   */
  addPoints: async (params: PointsAddParams): Promise<PointsRecord> => {
    const response = await apiClient.post<PointsRecord>('/members/points/add', params);
    return response.data;
  },

  /**
   * 减少积分
   */
  subtractPoints: async (params: PointsSubtractParams): Promise<PointsRecord> => {
    const response = await apiClient.post<PointsRecord>('/members/points/subtract', params);
    return response.data;
  },

  /**
   * 获取会员积分记录
   */
  getPointsRecords: async (memberId: number, page = 1, pageSize = 10): Promise<PointsRecordListResponse> => {
    const response = await apiClient.get<PointsRecordListResponse>(
      `/members/points/${memberId}?page=${page}&page_size=${pageSize}`
    );
    return response.data;
  },

  /**
   * 积分兑换
   */
  exchangePoints: async (params: PointsExchangeParams): Promise<PointsExchange> => {
    const response = await apiClient.post<PointsExchange>('/members/exchange', params);
    return response.data;
  },

  /**
   * 获取积分兑换记录
   */
  getExchanges: async (page = 1, pageSize = 10): Promise<PointsExchangeListResponse> => {
    const response = await apiClient.get<PointsExchangeListResponse>(
      `/members/exchanges?page=${page}&page_size=${pageSize}`
    );
    return response.data;
  },
};
