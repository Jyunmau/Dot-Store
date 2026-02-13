/**
 * 会员状态管理
 */
import { create } from 'zustand';
import type {
  Member,
  PointsRecord,
  PointsExchange,
  MemberCreateParams,
  MemberUpdateParams,
  PointsAddParams,
  PointsSubtractParams,
  PointsExchangeParams,
  MemberListResponse,
  PointsRecordListResponse,
  PointsExchangeListResponse,
} from '@/types/member';
import { memberService } from '@/services/memberService';

interface MemberState {
  members: Member[];
  currentMember: Member | null;
  pointsRecords: PointsRecord[];
  pointsExchanges: PointsExchange[];
  total: number;
  page: number;
  pageSize: number;
  isLoading: boolean;
  error: string | null;

  createMember: (data: MemberCreateParams) => Promise<Member>;
  listMembers: (params?: { page?: number; page_size?: number; level?: string; keyword?: string }) => Promise<void>;
  getMember: (memberId: number) => Promise<void>;
  updateMember: (memberId: number, data: MemberUpdateParams) => Promise<Member>;
  deleteMember: (memberId: number) => Promise<void>;
  addPoints: (params: PointsAddParams) => Promise<PointsRecord>;
  subtractPoints: (params: PointsSubtractParams) => Promise<PointsRecord>;
  getPointsRecords: (memberId: number, page?: number, pageSize?: number) => Promise<void>;
  exchangePoints: (params: PointsExchangeParams) => Promise<PointsExchange>;
  getExchanges: (page?: number, pageSize?: number) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

const initialState = {
  members: [],
  currentMember: null,
  pointsRecords: [],
  pointsExchanges: [],
  total: 0,
  page: 1,
  pageSize: 10,
  isLoading: false,
  error: null,
};

export const useMemberStore = create<MemberState>((set) => ({
  ...initialState,

  createMember: async (data: MemberCreateParams) => {
    set({ isLoading: true, error: null });
    try {
      const member = await memberService.createMember(data);
      set((state) => ({
        members: [member, ...state.members],
        total: state.total + 1,
        isLoading: false,
      }));
      return member;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '创建会员失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  listMembers: async (params?) => {
    set({ isLoading: true, error: null });
    try {
      const response: MemberListResponse = await memberService.listMembers(params);
      set({
        members: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取会员列表失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getMember: async (memberId: number) => {
    set({ isLoading: true, error: null });
    try {
      const member = await memberService.getMember(memberId);
      set({ currentMember: member, isLoading: false });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取会员详情失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updateMember: async (memberId: number, data: MemberUpdateParams) => {
    set({ isLoading: true, error: null });
    try {
      const member = await memberService.updateMember(memberId, data);
      set((state) => ({
        members: state.members.map((m) => (m.id === memberId ? member : m)),
        currentMember: state.currentMember?.id === memberId ? member : state.currentMember,
        isLoading: false,
      }));
      return member;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '更新会员失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  deleteMember: async (memberId: number) => {
    set({ isLoading: true, error: null });
    try {
      await memberService.deleteMember(memberId);
      set((state) => ({
        members: state.members.filter((m) => m.id !== memberId),
        total: state.total - 1,
        isLoading: false,
      }));
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '删除会员失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  addPoints: async (params: PointsAddParams) => {
    set({ isLoading: true, error: null });
    try {
      const record = await memberService.addPoints(params);
      set((state) => ({
        pointsRecords: [record, ...state.pointsRecords],
        members: state.members.map((m) =>
          m.id === params.member_id ? { ...m, points: m.points + params.points } : m
        ),
        currentMember:
          state.currentMember?.id === params.member_id
            ? { ...state.currentMember, points: state.currentMember.points + params.points }
            : state.currentMember,
        isLoading: false,
      }));
      return record;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '增加积分失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  subtractPoints: async (params: PointsSubtractParams) => {
    set({ isLoading: true, error: null });
    try {
      const record = await memberService.subtractPoints(params);
      set((state) => ({
        pointsRecords: [record, ...state.pointsRecords],
        members: state.members.map((m) =>
          m.id === params.member_id ? { ...m, points: m.points - params.points } : m
        ),
        currentMember:
          state.currentMember?.id === params.member_id
            ? { ...state.currentMember, points: state.currentMember.points - params.points }
            : state.currentMember,
        isLoading: false,
      }));
      return record;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '减少积分失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getPointsRecords: async (memberId: number, page = 1, pageSize = 10) => {
    set({ isLoading: true, error: null });
    try {
      const response: PointsRecordListResponse = await memberService.getPointsRecords(memberId, page, pageSize);
      set({
        pointsRecords: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取积分记录失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  exchangePoints: async (params: PointsExchangeParams) => {
    set({ isLoading: true, error: null });
    try {
      const exchange = await memberService.exchangePoints(params);
      set((state) => ({
        pointsExchanges: [exchange, ...state.pointsExchanges],
        members: state.members.map((m) =>
          m.id === params.member_id ? { ...m, points: m.points - params.points } : m
        ),
        currentMember:
          state.currentMember?.id === params.member_id
            ? { ...state.currentMember, points: state.currentMember.points - params.points }
            : state.currentMember,
        isLoading: false,
      }));
      return exchange;
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '积分兑换失败';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  getExchanges: async (page = 1, pageSize = 10) => {
    set({ isLoading: true, error: null });
    try {
      const response: PointsExchangeListResponse = await memberService.getExchanges(page, pageSize);
      set({
        pointsExchanges: response.items,
        total: response.total,
        page: response.page,
        pageSize: response.page_size,
        isLoading: false,
      });
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : '获取兑换记录失败';
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
