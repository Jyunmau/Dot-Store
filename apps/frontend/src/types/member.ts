/**
 * 会员相关类型定义
 */

/**
 * 会员接口
 */
export interface Member {
  id: number;
  user_id: number;
  name: string;
  phone: string;
  level: string;
  points: number;
  created_at: string;
  updated_at: string;
}

/**
 * 积分记录接口
 */
export interface PointsRecord {
  id: number;
  member_id: number;
  user_id: number;
  type: string;
  points: number;
  reason: string;
  created_at: string;
  member_name?: string;
}

/**
 * 积分兑换接口
 */
export interface PointsExchange {
  id: number;
  member_id: number;
  user_id: number;
  points: number;
  amount: string;
  created_at: string;
  member_name?: string;
}

/**
 * 创建会员参数
 */
export interface MemberCreateParams {
  name: string;
  phone: string;
  level?: string;
}

/**
 * 更新会员参数
 */
export interface MemberUpdateParams {
  name?: string;
  phone?: string;
  level?: string;
}

/**
 * 增加积分参数
 */
export interface PointsAddParams {
  member_id: number;
  points: number;
  reason: string;
}

/**
 * 减少积分参数
 */
export interface PointsSubtractParams {
  member_id: number;
  points: number;
  reason: string;
}

/**
 * 积分兑换参数
 */
export interface PointsExchangeParams {
  member_id: number;
  points: number;
  amount: number | string;
}

/**
 * 会员列表响应
 */
export interface MemberListResponse {
  items: Member[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 积分记录列表响应
 */
export interface PointsRecordListResponse {
  items: PointsRecord[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 积分兑换列表响应
 */
export interface PointsExchangeListResponse {
  items: PointsExchange[];
  total: number;
  page: number;
  page_size: number;
}

/**
 * 会员等级选项
 */
export const MEMBER_LEVEL_OPTIONS = [
  { value: 'normal', label: '普通会员' },
  { value: 'vip', label: 'VIP会员' },
];

/**
 * 获取会员等级显示名称
 */
export function getMemberLevelLabel(level: string): string {
  const option = MEMBER_LEVEL_OPTIONS.find(opt => opt.value === level);
  return option ? option.label : level;
}

/**
 * 积分类型选项
 */
export const POINTS_TYPE_OPTIONS = [
  { value: 'add', label: '增加' },
  { value: 'subtract', label: '减少' },
];

/**
 * 获取积分类型显示名称
 */
export function getPointsTypeLabel(type: string): string {
  const option = POINTS_TYPE_OPTIONS.find(opt => opt.value === type);
  return option ? option.label : type;
}
