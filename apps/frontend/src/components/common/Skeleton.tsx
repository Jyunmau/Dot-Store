/**
 * 骨架屏组件
 * 用于数据加载时的占位显示
 */
import React from 'react';

interface SkeletonProps {
  className?: string;
}

/**
 * 基础骨架屏
 */
export const Skeleton: React.FC<SkeletonProps> = ({ className = '' }) => (
  <div className={`skeleton rounded ${className}`} />
);

/**
 * 文本骨架屏
 */
export const SkeletonText: React.FC<{ rows?: number; className?: string }> = ({ 
  rows = 3, 
  className = '' 
}) => (
  <div className={`space-y-2 ${className}`}>
    {Array.from({ length: rows }).map((_, i) => (
      <div
        key={i}
        className="skeleton rounded h-4"
        style={{ width: i === rows - 1 ? '60%' : '100%' }}
      />
    ))}
  </div>
);

/**
 * 卡片骨架屏
 */
export const SkeletonCard: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
    <div className="flex items-center gap-3 mb-4">
      <Skeleton className="w-10 h-10 rounded-full" />
      <div className="flex-1">
        <Skeleton className="h-4 w-24 mb-2" />
        <Skeleton className="h-3 w-16" />
      </div>
    </div>
    <SkeletonText rows={2} />
  </div>
);

/**
 * 列表项骨架屏
 */
export const SkeletonListItem: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`flex items-center gap-3 p-3 border-b border-gray-100 ${className}`}>
    <Skeleton className="w-12 h-12 rounded-lg" />
    <div className="flex-1">
      <Skeleton className="h-4 w-32 mb-2" />
      <Skeleton className="h-3 w-24" />
    </div>
    <Skeleton className="w-16 h-6 rounded" />
  </div>
);

/**
 * 表格行骨架屏
 */
export const SkeletonTableRow: React.FC<{ columns?: number; className?: string }> = ({ 
  columns = 4, 
  className = '' 
}) => (
  <tr className={className}>
    {Array.from({ length: columns }).map((_, i) => (
      <td key={i} className="p-3">
        <Skeleton className="h-4 w-full" />
      </td>
    ))}
  </tr>
);

/**
 * 统计卡片骨架屏
 */
export const SkeletonStatCard: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
    <Skeleton className="h-4 w-20 mb-3" />
    <Skeleton className="h-8 w-32 mb-2" />
    <Skeleton className="h-3 w-24" />
  </div>
);

/**
 * 图表骨架屏
 */
export const SkeletonChart: React.FC<{ className?: string }> = ({ className = '' }) => (
  <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
    <div className="flex justify-between items-center mb-4">
      <Skeleton className="h-5 w-24" />
      <Skeleton className="h-8 w-20 rounded" />
    </div>
    <div className="flex items-end gap-2 h-40">
      {Array.from({ length: 7 }).map((_, i) => (
        <div
          key={i}
          className="skeleton rounded-t flex-1"
          style={{ height: `${30 + Math.random() * 70}%` }}
        />
      ))}
    </div>
  </div>
);

/**
 * 页面骨架屏
 */
export const SkeletonPage: React.FC = () => (
  <div className="p-4 md:p-6">
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {Array.from({ length: 4 }).map((_, i) => (
        <SkeletonStatCard key={i} />
      ))}
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <SkeletonChart />
      <SkeletonChart />
    </div>
  </div>
);

export default Skeleton;
