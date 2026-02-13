/**
 * 下拉刷新组件
 * 支持移动端下拉刷新操作
 */
import React, { useState, useCallback, useRef } from 'react';
import { LoadingOutlined } from '@ant-design/icons';

interface PullToRefreshProps {
  onRefresh: () => Promise<void>;
  children: React.ReactNode;
  disabled?: boolean;
}

const PullToRefresh: React.FC<PullToRefreshProps> = ({
  onRefresh,
  children,
  disabled = false,
}) => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [pullDistance, setPullDistance] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const startY = useRef(0);
  const isPulling = useRef(false);

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (disabled || isRefreshing) return;
    
    const container = containerRef.current;
    if (!container || container.scrollTop > 0) return;
    
    startY.current = e.touches[0].clientY;
    isPulling.current = true;
  }, [disabled, isRefreshing]);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (!isPulling.current || disabled || isRefreshing) return;
    
    const currentY = e.touches[0].clientY;
    const distance = currentY - startY.current;
    
    if (distance > 0) {
      const pullDist = Math.min(distance * 0.5, 80);
      setPullDistance(pullDist);
    }
  }, [disabled, isRefreshing]);

  const handleTouchEnd = useCallback(async () => {
    if (!isPulling.current || disabled || isRefreshing) return;
    
    isPulling.current = false;
    
    if (pullDistance >= 60) {
      setIsRefreshing(true);
      try {
        await onRefresh();
      } finally {
        setIsRefreshing(false);
      }
    }
    
    setPullDistance(0);
  }, [pullDistance, disabled, isRefreshing, onRefresh]);

  return (
    <div
      ref={containerRef}
      className="relative overflow-auto"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      style={{
        transform: `translateY(${pullDistance}px)`,
        transition: isPulling.current ? 'none' : 'transform 0.2s ease-out',
      }}
    >
      {/* 下拉刷新指示器 */}
      {(pullDistance > 0 || isRefreshing) && (
        <div
          className="absolute left-1/2 -translate-x-1/2 flex items-center justify-center"
          style={{
            top: -50 + pullDistance,
            opacity: Math.min(pullDistance / 60, 1),
          }}
        >
          <div className="w-10 h-10 rounded-full bg-white shadow-md flex items-center justify-center">
            {isRefreshing ? (
              <LoadingOutlined className="text-blue-500 text-lg" spin />
            ) : (
              <svg
                className="w-5 h-5 text-blue-500"
                style={{
                  transform: `rotate(${pullDistance * 2}deg)`,
                  transition: 'transform 0.1s',
                }}
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
              </svg>
            )}
          </div>
        </div>
      )}
      
      {children}
    </div>
  );
};

export default PullToRefresh;
