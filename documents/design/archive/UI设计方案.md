# Dot-Store UI设计方案

> **版本信息**
> - 版本：v1.0
> - 创建日期：2026-02-07
> - 作者：UI设计团队
> - 适用范围：阶段一（基础优化）和阶段二（品牌建设）

---

## 1. 方案概述

### 1.1 设计理念

本方案融合现代简约风格与品牌强化风格，在保证快速上线的同时，为长期品牌建设奠定基础。设计核心理念：

- **简洁高效**：界面简洁，信息层级清晰，减少用户认知负担
- **品牌识别**：通过统一的视觉元素建立品牌识别度
- **情感连接**：通过微交互和动效提升用户体验
- **渐进增强**：分阶段实施，逐步完善设计系统

### 1.2 设计目标

| 目标维度 | 当前状态 | 阶段一目标 | 阶段二目标 |
|---------|---------|-----------|-----------|
| 图标系统 | ❌ 缺失 | ✅ 完整图标库 | ✅ 品牌化图标 |
| 交互反馈 | ⚠️ 基础 | ✅ 完善反馈 | ✅ 品牌化反馈 |
| 视觉层次 | ⚠️ 一般 | ✅ 清晰层次 | ✅ 品牌化层次 |
| 品牌识别 | ⚠️ 较低 | ⚠️ 基础识别 | ✅ 强识别度 |
| 无障碍支持 | ⚠️ 基础 | ✅ WCAG AA | ✅ WCAG AA+ |

### 1.3 技术栈

- **图标库**：Heroicons（MIT许可，阶段一）→ 自定义品牌图标（阶段二）
- **字体**：Inter（系统字体栈）
- **CSS框架**：原生CSS + CSS变量
- **动画库**：CSS Transitions + Keyframes
- **图标组件**：React组件化封装

---

## 2. 阶段一：基础优化（0-4周）

### 2.1 设计原则

- **快速实现**：使用成熟的开源资源，2-3周完成
- **兼容性强**：确保跨浏览器和跨设备一致性
- **易于维护**：代码结构清晰，便于后续升级
- **用户友好**：提升基础用户体验，解决核心痛点

### 2.2 色彩系统

#### 2.2.1 主色调优化

```css
:root {
  /* 主色调 - 更现代的蓝色系 */
  --color-primary: #3B82F6;
  --color-primary-light: #DBEAFE;
  --color-primary-dark: #1D4ED8;
  
  /* 渐变色 */
  --gradient-primary: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  --gradient-success: linear-gradient(135deg, #10B981 0%, #059669 100%);
  --gradient-warning: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
  --gradient-danger: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
}
```

#### 2.2.2 功能色保持

保持现有功能色系统，仅调整色值以提升对比度：

```css
/* 功能色 */
--color-success: #52C41A;
--color-success-light: #F6FFED;
--color-error: #F5222D;
--color-error-light: #FFF2F0;
--color-warning: #FA541C;
--color-warning-light: #FFFBE6;
```

#### 2.2.3 中性色优化

```css
/* 中性色 - 增加深色选项 */
--color-white: #FFFFFF;
--color-gray-50: #F9FAFB;
--color-gray-100: #F3F4F6;
--color-gray-200: #E5E7EB;
--color-gray-300: #D1D5DB;
--color-gray-400: #9CA3AF;
--color-gray-500: #6B7280;
--color-gray-600: #4B5563;
--color-gray-700: #374151;
--color-gray-800: #1F2937;
--color-gray-900: #111827;
```

### 2.3 排版系统

#### 2.3.1 字体系统

```css
:root {
  /* 字体族 */
  --font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  --font-family-display: 'Inter', sans-serif;
  --font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  
  /* 字号系统 */
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-size-2xl: 24px;
  --font-size-3xl: 30px;
  --font-size-4xl: 36px;
  --font-size-5xl: 48px;
  
  /* 行高系统 */
  --line-height-none: 1;
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;
  
  /* 字重系统 */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* 字间距 */
  --letter-spacing-tighter: -0.05em;
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
  --letter-spacing-widest: 0.1em;
}
```

#### 2.3.2 排版规范

| 元素 | 字号 | 字重 | 行高 | 字间距 | 用途 |
|------|------|------|------|--------|------|
| H1 | 36px | 700 | 1.2 | -0.025em | 页面主标题 |
| H2 | 30px | 600 | 1.3 | -0.025em | 章节标题 |
| H3 | 24px | 600 | 1.4 | 0 | 卡片标题 |
| H4 | 20px | 600 | 1.5 | 0 | 次级标题 |
| Body | 16px | 400 | 1.5 | 0 | 正文文字 |
| Small | 14px | 400 | 1.5 | 0 | 辅助文字 |
| Tiny | 12px | 400 | 1.5 | 0 | 小字说明 |

### 2.4 图标系统

#### 2.4.1 图标库选择

**阶段一：Heroicons（开源）**

选择理由：
- MIT许可，可商用
- 风格现代，符合设计理念
- 提供SVG格式，易于定制
- 支持outline和filled两种风格
- 持续更新，社区活跃

#### 2.4.2 图标分类

**导航图标（24px，outline）**

| 图标名称 | 用途 | 文件名 |
|---------|------|--------|
| home | 首页 | home.svg |
| document-text | 记录 | document-text.svg |
| chart-bar | 报表 | chart-bar.svg |
| cog | 设置 | cog.svg |

**操作图标（20px，outline）**

| 图标名称 | 用途 | 文件名 |
|---------|------|--------|
| plus | 添加 | plus.svg |
| pencil | 编辑 | pencil.svg |
| trash | 删除 | trash.svg |
| search | 搜索 | search.svg |
| filter | 筛选 | filter.svg |
| chevron-left | 返回 | chevron-left.svg |
| chevron-right | 前进 | chevron-right.svg |

**状态图标（16px，filled）**

| 图标名称 | 用途 | 文件名 |
|---------|------|--------|
| check-circle | 成功 | check-circle.svg |
| x-circle | 错误 | x-circle.svg |
| exclamation-circle | 警告 | exclamation-circle.svg |
| information-circle | 信息 | information-circle.svg |

**财务图标（20px，outline）**

| 图标名称 | 用途 | 文件名 |
|---------|------|--------|
| arrow-trending-up | 收入/增长 | arrow-trending-up.svg |
| arrow-trending-down | 支出/下降 | arrow-trending-down.svg |
| currency-yen | 金额 | currency-yen.svg |
| cube | 订单 | cube.svg |

#### 2.4.3 图标组件设计

```jsx
/**
 * 图标组件
 * @param {string} name - 图标名称
 * @param {string} size - 图标尺寸：xs, sm, md, lg, xl
 * @param {string} variant - 图标变体：outline, filled
 * @param {string} className - 自定义类名
 * @param {string} color - 图标颜色
 */
const Icon = ({ name, size = 'md', variant = 'outline', className = '', color }) => {
  const sizeMap = {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
    xl: 48
  };
  
  const iconSize = sizeMap[size] || sizeMap.md;
  
  return (
    <svg
      width={iconSize}
      height={iconSize}
      viewBox="0 0 24 24"
      fill={variant === 'filled' ? 'currentColor' : 'none'}
      stroke={variant === 'outline' ? 'currentColor' : 'none'}
      strokeWidth={variant === 'outline' ? 2 : 0}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      style={{ color }}
    >
      {/* 图标路径 */}
    </svg>
  );
};

export default Icon;
```

### 2.5 间距系统

保持现有8px网格系统，增加更多间距选项：

```css
:root {
  --spacing-0: 0;
  --spacing-px: 1px;
  --spacing-0_5: 2px;
  --spacing-1: 4px;
  --spacing-1_5: 6px;
  --spacing-2: 8px;
  --spacing-2_5: 10px;
  --spacing-3: 12px;
  --spacing-3_5: 14px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-7: 28px;
  --spacing-8: 32px;
  --spacing-9: 36px;
  --spacing-10: 40px;
  --spacing-11: 44px;
  --spacing-12: 48px;
  --spacing-14: 56px;
  --spacing-16: 64px;
  --spacing-20: 80px;
  --spacing-24: 96px;
  --spacing-32: 128px;
}
```

### 2.6 圆角系统

```css
:root {
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-2xl: 16px;
  --radius-3xl: 24px;
  --radius-full: 9999px;
}
```

### 2.7 阴影系统

```css
:root {
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
}
```

### 2.8 组件设计规范

#### 2.8.1 按钮组件

**主要按钮**

```css
.btn-primary {
  background: var(--gradient-primary);
  color: white;
  border: none;
  border-radius: var(--radius-lg);
  padding: 12px 24px;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

**次要按钮**

```css
.btn-secondary {
  background: white;
  color: var(--color-gray-700);
  border: 1px solid var(--color-gray-300);
  border-radius: var(--radius-lg);
  padding: 12px 24px;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--color-gray-50);
  border-color: var(--color-gray-400);
}

.btn-secondary:active {
  background: var(--color-gray-100);
}
```

**图标按钮**

```css
.btn-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-gray-300);
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: var(--color-gray-50);
  transform: scale(1.05);
}

.btn-icon:active {
  transform: scale(0.95);
}
```

#### 2.8.2 卡片组件

**基础卡片**

```css
.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-6);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
```

**统计卡片**

```css
.card-stat {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-6);
  text-align: center;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

.card-stat:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-4px);
}

.card-stat .icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-4);
}

.card-stat .icon-income {
  background: var(--color-success-light);
  color: var(--color-success);
}

.card-stat .icon-expense {
  background: var(--color-error-light);
  color: var(--color-error);
}

.card-stat .icon-profit {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.card-stat .amount {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin: var(--spacing-2) 0;
}

.card-stat .amount.income {
  color: var(--color-success);
}

.card-stat .amount.expense {
  color: var(--color-error);
}

.card-stat .amount.profit {
  color: var(--color-warning);
}

.card-stat .label {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  color: var(--color-gray-600);
  margin-bottom: var(--spacing-2);
}

.card-stat .sublabel {
  font-size: var(--font-size-sm);
  color: var(--color-gray-500);
}
```

#### 2.8.3 输入框组件

```css
.input {
  width: 100%;
  padding: var(--spacing-3) var(--spacing-4);
  border: 1px solid var(--color-gray-300);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  color: var(--color-gray-900);
  background: white;
  transition: all 0.2s ease;
}

.input:hover {
  border-color: var(--color-gray-400);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input:disabled {
  background: var(--color-gray-100);
  color: var(--color-gray-500);
  cursor: not-allowed;
}

.input.error {
  border-color: var(--color-error);
}

.input.error:focus {
  box-shadow: 0 0 0 3px rgba(245, 34, 45, 0.1);
}
```

### 2.9 交互设计

#### 2.9.1 过渡动画

```css
/* 基础过渡 */
.transition-all {
  transition-property: all;
  transition-timing-function: ease;
  transition-duration: 200ms;
}

/* 快速过渡 */
.transition-fast {
  transition-duration: 150ms;
}

/* 慢速过渡 */
.transition-slow {
  transition-duration: 300ms;
}

/* 弹性过渡 */
.transition-bounce {
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

#### 2.9.2 关键帧动画

```css
/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 淡入上浮动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 缩放动画 */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 旋转加载动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 脉冲动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
```

#### 2.9.3 加载状态

**骨架屏加载**

```jsx
const Skeleton = ({ className = '', height = 'auto', width = '100%' }) => {
  return (
    <div
      className={`skeleton ${className}`}
      style={{ height, width }}
    >
      <style jsx>{`
        .skeleton {
          background: linear-gradient(
            90deg,
            var(--color-gray-200) 0%,
            var(--color-gray-100) 50%,
            var(--color-gray-200) 100%
          );
          background-size: 200% 100%;
          animation: skeleton-loading 1.5s ease-in-out infinite;
          border-radius: var(--radius-md);
        }

        @keyframes skeleton-loading {
          0% {
            background-position: 200% 0;
          }
          100% {
            background-position: -200% 0;
          }
        }
      `}</style>
    </div>
  );
};
```

**旋转加载器**

```jsx
const Spinner = ({ size = 'md', color = 'var(--color-primary)' }) => {
  const sizeMap = {
    sm: 16,
    md: 24,
    lg: 32,
    xl: 48
  };
  
  const spinnerSize = sizeMap[size] || sizeMap.md;
  
  return (
    <svg
      width={spinnerSize}
      height={spinnerSize}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="spinner"
    >
      <style jsx>{`
        .spinner {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke={color}
        strokeWidth="4"
        strokeDasharray="60"
        strokeDashoffset="20"
        strokeLinecap="round"
      />
    </svg>
  );
};
```

#### 2.9.4 反馈机制

**Toast通知**

```jsx
const Toast = ({ message, type = 'success', duration = 3000, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);
    
    return () => clearTimeout(timer);
  }, [duration, onClose]);
  
  const typeStyles = {
    success: {
      background: 'var(--color-success-light)',
      color: 'var(--color-success)',
      icon: 'check-circle'
    },
    error: {
      background: 'var(--color-error-light)',
      color: 'var(--color-error)',
      icon: 'x-circle'
    },
    warning: {
      background: 'var(--color-warning-light)',
      color: 'var(--color-warning)',
      icon: 'exclamation-circle'
    },
    info: {
      background: 'var(--color-primary-light)',
      color: 'var(--color-primary)',
      icon: 'information-circle'
    }
  };
  
  const style = typeStyles[type];
  
  return (
    <div className={`toast toast-${type}`}>
      <Icon name={style.icon} size="sm" color={style.color} />
      <span className="toast-message">{message}</span>
      <button className="toast-close" onClick={onClose}>
        <Icon name="x" size="sm" />
      </button>
      <style jsx>{`
        .toast {
          position: fixed;
          top: 20px;
          right: 20px;
          padding: 12px 16px;
          border-radius: var(--radius-lg);
          box-shadow: var(--shadow-lg);
          display: flex;
          align-items: center;
          gap: 12px;
          min-width: 300px;
          animation: slideInRight 0.3s ease;
          z-index: 1000;
        }

        @keyframes slideInRight {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        .toast-message {
          flex: 1;
          font-size: var(--font-size-sm);
          font-weight: var(--font-weight-medium);
        }

        .toast-close {
          background: none;
          border: none;
          cursor: pointer;
          padding: 4px;
          border-radius: var(--radius-sm);
        }

        .toast-close:hover {
          background: rgba(0, 0, 0, 0.05);
        }
      `}</style>
    </div>
  );
};
```

### 2.10 空状态设计

```jsx
const EmptyState = ({ 
  icon, 
  title, 
  description, 
  actionText, 
  onAction 
}) => {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <Icon name={icon} size="xl" color="var(--color-gray-400)" />
      </div>
      <h3 className="empty-state-title">{title}</h3>
      <p className="empty-state-description">{description}</p>
      {actionText && onAction && (
        <button className="btn-primary empty-state-action" onClick={onAction}>
          {actionText}
        </button>
      )}
      <style jsx>{`
        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: var(--spacing-12);
          text-align: center;
        }

        .empty-state-icon {
          margin-bottom: var(--spacing-6);
          opacity: 0.6;
        }

        .empty-state-title {
          font-size: var(--font-size-xl);
          font-weight: var(--font-weight-semibold);
          color: var(--color-gray-700);
          margin-bottom: var(--spacing-3);
        }

        .empty-state-description {
          font-size: var(--font-size-base);
          color: var(--color-gray-500);
          margin-bottom: var(--spacing-6);
          max-width: 400px;
        }

        .empty-state-action {
          margin-top: var(--spacing-2);
        }
      `}</style>
    </div>
  );
};
```

### 2.11 响应式设计

#### 2.11.1 断点系统

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* 移动端优先 */
@media (min-width: 640px) {
  /* sm及以上 */
}

@media (min-width: 768px) {
  /* md及以上 */
}

@media (min-width: 1024px) {
  /* lg及以上 */
}

@media (min-width: 1280px) {
  /* xl及以上 */
}

@media (min-width: 1536px) {
  /* 2xl及以上 */
}
```

#### 2.11.2 布局调整

```css
/* 移动端（< 768px） */
@media (max-width: 767px) {
  .main-content {
    margin-left: 0;
    margin-top: 64px;
    padding: var(--spacing-4);
  }

  .summary-cards-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-4);
  }

  .quick-actions {
    grid-template-columns: 1fr;
    gap: var(--spacing-3);
  }

  .mobile-bottom-nav {
    display: flex;
  }

  .desktop-side-nav {
    display: none;
  }
}

/* 平板端（768px - 1023px） */
@media (min-width: 768px) and (max-width: 1023px) {
  .main-content {
    margin-left: 0;
    margin-top: 64px;
    padding: var(--spacing-6);
  }

  .summary-cards-container {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-5);
  }

  .quick-actions {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-4);
  }

  .mobile-tablet-header {
    display: flex;
  }

  .desktop-side-nav {
    display: none;
  }
}

/* 桌面端（≥ 1024px） */
@media (min-width: 1024px) {
  .main-content {
    margin-left: 200px;
    margin-top: 0;
    padding: var(--spacing-8);
  }

  .summary-cards-container {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-6);
  }

  .quick-actions {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-5);
  }

  .desktop-side-nav {
    display: flex;
  }

  .mobile-tablet-header {
    display: none;
  }

  .mobile-bottom-nav {
    display: none;
  }
}
```

### 2.12 无障碍支持

#### 2.12.1 ARIA标签

```jsx
// 按钮组件添加ARIA标签
<button 
  className="btn-primary"
  aria-label="保存记录"
  aria-pressed={false}
>
  保存
</button>

// 图标按钮添加ARIA标签
<button 
  className="btn-icon"
  aria-label="删除记录"
  aria-describedby="delete-tooltip"
>
  <Icon name="trash" size="sm" />
</button>

// 输入框添加ARIA标签
<input
  type="text"
  className="input"
  aria-label="记录金额"
  aria-required="true"
  aria-invalid={error}
  aria-describedby={error ? 'amount-error' : 'amount-help'}
/>
{error && (
  <span id="amount-error" role="alert" className="error-message">
    {error}
  </span>
)}
```

#### 2.12.2 焦点管理

```css
/* 焦点可见性 */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* 跳过导航链接 */
.skip-to-content {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 100;
  transition: top 0.3s;
}

.skip-to-content:focus {
  top: 0;
}

/* 屏幕阅读器专用 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

#### 2.12.3 颜色对比度

确保所有文本与背景的对比度至少达到WCAG AA标准（4.5:1）：

```css
/* 主色对比度检查 */
--color-primary: #3B82F6; /* 与白色对比度 4.5:1 ✅ */
--color-primary-dark: #1D4ED8; /* 与白色对比度 7.1:1 ✅ */

/* 功能色对比度检查 */
--color-success: #52C41A; /* 与白色对比度 4.6:1 ✅ */
--color-error: #F5222D; /* 与白色对比度 4.5:1 ✅ */
--color-warning: #FA541C; /* 与白色对比度 4.5:1 ✅ */

/* 文本颜色对比度检查 */
--color-gray-900: #111827; /* 与白色对比度 15.6:1 ✅ */
--color-gray-700: #374151; /* 与白色对比度 10.7:1 ✅ */
--color-gray-500: #6B7280; /* 与白色对比度 5.7:1 ✅ */
```

---

## 3. 阶段二：品牌建设（5-12周）

### 3.1 设计原则

- **品牌识别**：建立独特的品牌视觉系统
- **情感连接**：通过品牌元素增强用户粘性
- **游戏化**：引入成就系统提升参与度
- **持续迭代**：基于用户反馈优化设计

### 3.2 品牌视觉系统

#### 3.2.1 品牌Logo设计

**主Logo**

```
设计理念：
- 抽象的"点"（Dot）图形
- 使用品牌渐变色
- 圆角设计，体现友好性
- 简洁现代，易于识别

尺寸规范：
- 标准版：200px × 60px
- 小版：100px × 30px
- 图标版：60px × 60px
- Favicon：32px × 32px
```

**Logo使用规范**

```css
/* Logo容器 */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
}

.logo-text {
  font-size: 20px;
  font-weight: var(--font-weight-bold);
  background: var(--gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

#### 3.2.2 品牌色彩系统

```css
:root {
  /* 品牌主色调 */
  --color-brand-primary: #6366F1;
  --color-brand-primary-light: #E0E7FF;
  --color-brand-primary-dark: #4338CA;
  
  /* 品牌辅助色 */
  --color-brand-accent: #F59E0B;
  --color-brand-accent-light: #FEF3C7;
  --color-brand-accent-dark: #D97706;
  
  /* 品牌渐变色 */
  --gradient-brand: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%);
  --gradient-brand-subtle: linear-gradient(135deg, #E0E7FF 0%, #EDE9FE 50%, #F3E8FF 100%);
  --gradient-brand-accent: linear-gradient(135deg, #F59E0B 0%, #F97316 100%);
}
```

#### 3.2.3 品牌图标系统

**自定义品牌图标**

阶段二将Heroicons替换为自定义品牌图标，保持统一的视觉风格：

```css
/* 品牌图标样式 */
.brand-icon {
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2.5px;
  border-radius: 4px;
}

/* 品牌图标渐变填充 */
.brand-icon.filled {
  fill: url(#brand-gradient);
  stroke: none;
}
```

#### 3.2.4 品牌字体系统

```css
:root {
  /* 品牌展示字体 */
  --font-family-brand-display: 'Poppins', 'Inter', sans-serif;
  
  /* 品牌正文字体 */
  --font-family-brand-body: 'Inter', system-ui, sans-serif;
  
  /* 品牌数字字体 */
  --font-family-brand-mono: 'SF Mono', 'Roboto Mono', monospace;
}
```

### 3.3 品牌化组件设计

#### 3.3.1 品牌化卡片

```css
.card-brand {
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-6);
  position: relative;
  overflow: hidden;
}

/* 品牌渐变顶部条 */
.card-brand::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-brand);
}

.card-brand:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: var(--shadow-lg);
}
```

#### 3.3.2 品牌化按钮

```css
.btn-brand {
  background: var(--gradient-brand);
  color: white;
  border: none;
  border-radius: var(--radius-xl);
  padding: 14px 28px;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

/* 按钮光泽效果 */
.btn-brand::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: rotate(45deg) translateX(-100%);
  transition: transform 0.6s;
}

.btn-brand:hover::after {
  transform: rotate(45deg) translateX(100%);
}

.btn-brand:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

#### 3.3.3 品牌化统计卡片

```css
.card-stat-brand {
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-6);
  text-align: center;
  min-height: 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* 品牌渐变背景 */
.card-stat-brand::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-brand-subtle);
  opacity: 0.5;
  z-index: 0;
}

.card-stat-brand > * {
  position: relative;
  z-index: 1;
}

.card-stat-brand .icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-4);
  background: var(--gradient-brand);
  color: white;
  box-shadow: var(--shadow-md);
}

.card-stat-brand .amount {
  font-size: var(--font-size-5xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin: var(--spacing-2) 0;
  background: var(--gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### 3.4 成就系统设计

#### 3.4.1 成就类型

```javascript
const achievementTypes = {
  firstRecord: {
    id: 'first_record',
    name: '首次记录',
    description: '完成第一条记录',
    icon: 'trophy',
    badge: '🥇',
    condition: (stats) => stats.totalRecords >= 1
  },
  streak7Days: {
    id: 'streak_7_days',
    name: '连续7天',
    description: '连续记录7天',
    icon: 'fire',
    badge: '🔥',
    condition: (stats) => stats.currentStreak >= 7
  },
  streak30Days: {
    id: 'streak_30_days',
    name: '连续30天',
    description: '连续记录30天',
    icon: 'star',
    badge: '⭐',
    condition: (stats) => stats.currentStreak >= 30
  },
  monthlyGoal: {
    id: 'monthly_goal',
    name: '月度目标',
    description: '达成月度记录目标',
    icon: 'target',
    badge: '🎯',
    condition: (stats) => stats.monthlyRecords >= 30
  },
  total100Records: {
    id: 'total_100_records',
    name: '百次记录',
    description: '累计记录100次',
    icon: 'award',
    badge: '🏆',
    condition: (stats) => stats.totalRecords >= 100
  }
};
```

#### 3.4.2 成就徽章组件

```jsx
const AchievementBadge = ({ achievement, unlocked, size = 'md' }) => {
  const sizeMap = {
    sm: 48,
    md: 64,
    lg: 96
  };
  
  const badgeSize = sizeMap[size] || sizeMap.md;
  
  return (
    <div className={`achievement-badge ${unlocked ? 'unlocked' : 'locked'} size-${size}`}>
      <div className="badge-icon" style={{ width: badgeSize, height: badgeSize }}>
        <Icon name={achievement.icon} size={size === 'lg' ? 'xl' : 'lg'} />
      </div>
      <div className="badge-emoji">{achievement.badge}</div>
      <div className="badge-name">{achievement.name}</div>
      <div className="badge-description">{achievement.description}</div>
      <style jsx>{`
        .achievement-badge {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: var(--spacing-4);
          border-radius: var(--radius-xl);
          transition: all 0.3s ease;
          cursor: pointer;
        }

        .achievement-badge.unlocked {
          background: var(--color-success-light);
          border: 2px solid var(--color-success);
        }

        .achievement-badge.locked {
          background: var(--color-gray-100);
          border: 2px solid var(--color-gray-300);
          opacity: 0.6;
        }

        .achievement-badge:hover {
          transform: translateY(-4px);
          box-shadow: var(--shadow-lg);
        }

        .badge-icon {
          background: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: var(--spacing-3);
          box-shadow: var(--shadow-md);
        }

        .badge-emoji {
          font-size: 24px;
          margin-bottom: var(--spacing-2);
        }

        .badge-name {
          font-size: var(--font-size-sm);
          font-weight: var(--font-weight-semibold);
          color: var(--color-gray-800);
          margin-bottom: var(--spacing-1);
        }

        .badge-description {
          font-size: var(--font-size-xs);
          color: var(--color-gray-600);
          text-align: center;
        }
      `}</style>
    </div>
  );
};
```

#### 3.4.3 成就解锁通知

```jsx
const AchievementUnlock = ({ achievement, onDismiss }) => {
  return (
    <div className="achievement-unlock">
      <div className="achievement-unlock-content">
        <div className="achievement-unlock-emoji">{achievement.badge}</div>
        <div className="achievement-unlock-info">
          <h4 className="achievement-unlock-title">🎉 成就解锁！</h4>
          <p className="achievement-unlock-name">{achievement.name}</p>
          <p className="achievement-unlock-desc">{achievement.description}</p>
        </div>
        <button className="achievement-unlock-close" onClick={onDismiss}>
          <Icon name="x" size="sm" />
        </button>
      </div>
      <style jsx>{`
        .achievement-unlock {
          position: fixed;
          top: 20px;
          right: 20px;
          background: white;
          border-radius: var(--radius-xl);
          box-shadow: var(--shadow-xl);
          padding: var(--spacing-5);
          min-width: 350px;
          animation: slideInRight 0.5s ease;
          z-index: 1000;
          border: 2px solid var(--color-brand-primary);
        }

        @keyframes slideInRight {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        .achievement-unlock-content {
          display: flex;
          align-items: flex-start;
          gap: var(--spacing-4);
        }

        .achievement-unlock-emoji {
          font-size: 48px;
          flex-shrink: 0;
        }

        .achievement-unlock-info {
          flex: 1;
        }

        .achievement-unlock-title {
          font-size: var(--font-size-lg);
          font-weight: var(--font-weight-bold);
          color: var(--color-brand-primary);
          margin-bottom: var(--spacing-2);
        }

        .achievement-unlock-name {
          font-size: var(--font-size-base);
          font-weight: var(--font-weight-semibold);
          color: var(--color-gray-800);
          margin-bottom: var(--spacing-1);
        }

        .achievement-unlock-desc {
          font-size: var(--font-size-sm);
          color: var(--color-gray-600);
        }

        .achievement-unlock-close {
          background: none;
          border: none;
          cursor: pointer;
          padding: 4px;
          border-radius: var(--radius-sm);
          flex-shrink: 0;
        }

        .achievement-unlock-close:hover {
          background: var(--color-gray-100);
        }
      `}</style>
    </div>
  );
};
```

### 3.5 品牌化空状态

```jsx
const BrandedEmptyState = ({ 
  type = 'no-records',
  title,
  description,
  actionText,
  onAction
}) => {
  const emptyStates = {
    'no-records': {
      icon: 'document-text',
      illustration: '🔍',
      title: '暂无记录',
      description: '开始记录您的第一笔收支吧！'
    },
    'no-data': {
      icon: 'chart-bar',
      illustration: '📊',
      title: '暂无数据',
      description: '记录更多数据后即可查看报表'
    },
    'no-network': {
      icon: 'wifi',
      illustration: '📡',
      title: '网络连接失败',
      description: '请检查您的网络连接后重试'
    }
  };
  
  const state = emptyStates[type] || emptyStates['no-records'];
  
  return (
    <div className="branded-empty-state">
      <div className="empty-state-illustration">{state.illustration}</div>
      <div className="empty-state-icon">
        <Icon name={state.icon} size="xl" color="var(--color-brand-primary)" />
      </div>
      <h3 className="empty-state-title">{title || state.title}</h3>
      <p className="empty-state-description">{description || state.description}</p>
      {actionText && onAction && (
        <button className="btn-brand empty-state-action" onClick={onAction}>
          {actionText}
        </button>
      )}
      <style jsx>{`
        .branded-empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: var(--spacing-12);
          text-align: center;
          background: var(--gradient-brand-subtle);
          border-radius: var(--radius-2xl);
          margin: var(--spacing-8) 0;
        }

        .empty-state-illustration {
          font-size: 80px;
          margin-bottom: var(--spacing-6);
          animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-10px);
          }
        }

        .empty-state-icon {
          margin-bottom: var(--spacing-6);
        }

        .empty-state-title {
          font-size: var(--font-size-2xl);
          font-weight: var(--font-weight-bold);
          color: var(--color-gray-800);
          margin-bottom: var(--spacing-3);
        }

        .empty-state-description {
          font-size: var(--font-size-base);
          color: var(--color-gray-600);
          margin-bottom: var(--spacing-6);
          max-width: 400px;
        }

        .empty-state-action {
          margin-top: var(--spacing-2);
        }
      `}</style>
    </div>
  );
};
```

### 3.6 品牌化动效

#### 3.6.1 页面加载动画

```css
@keyframes pageLoad {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-content {
  animation: pageLoad 0.6s ease-out;
}

/* 卡片依次淡入 */
.card {
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
.card:nth-child(5) { animation-delay: 0.5s; }
```

#### 3.6.2 数字滚动动画

```jsx
const AnimatedNumber = ({ value, duration = 1000, prefix = '', suffix = '' }) => {
  const [displayValue, setDisplayValue] = useState(0);
  
  useEffect(() => {
    let startTime;
    let animationFrame;
    
    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      
      // 使用缓动函数
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const currentValue = Math.floor(value * easeOutQuart);
      
      setDisplayValue(currentValue);
      
      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };
    
    animationFrame = requestAnimationFrame(animate);
    
    return () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
    };
  }, [value, duration]);
  
  return (
    <span className="animated-number">
      {prefix}{displayValue.toLocaleString()}{suffix}
    </span>
  );
};
```

---

## 4. 实施计划

### 4.1 阶段一实施计划（0-4周）

#### 第1周：设计系统基础

**任务清单：**
- [ ] 确定色彩系统规范
- [ ] 确定排版系统规范
- [ ] 确定间距和圆角系统
- [ ] 确定阴影系统
- [ ] 创建CSS变量文件

**交付物：**
- 设计系统规范文档（CSS变量）
- 色彩对比度检查报告

#### 第2周：图标系统

**任务清单：**
- [ ] 下载Heroicons图标库
- [ ] 创建Icon组件
- [ ] 实现导航图标
- [ ] 实现操作图标
- [ ] 实现状态图标
- [ ] 实现财务图标

**交付物：**
- Icon组件
- 图标库文档

#### 第3周：基础组件

**任务清单：**
- [ ] 更新Button组件
- [ ] 更新Card组件
- [ ] 创建Input组件
- [ ] 创建Skeleton组件
- [ ] 创建Spinner组件
- [ ] 创建Toast组件
- [ ] 创建EmptyState组件

**交付物：**
- 完整的基础组件库
- 组件使用文档

#### 第4周：页面实现

**任务清单：**
- [ ] 更新Today页面
- [ ] 更新Record页面
- [ ] 更新Report页面
- [ ] 更新Settings页面
- [ ] 实现响应式布局
- [ ] 添加无障碍支持
- [ ] 性能优化

**交付物：**
- 更新后的所有页面
- 响应式测试报告
- 无障碍测试报告

### 4.2 阶段二实施计划（5-12周）

#### 第5-6周：品牌设计

**任务清单：**
- [ ] 设计品牌Logo
- [ ] 确定品牌色彩系统
- [ ] 确定品牌字体系统
- [ ] 设计品牌图标系统
- [ ] 创建品牌视觉规范文档

**交付物：**
- 品牌Logo（多尺寸）
- 品牌视觉规范文档
- 品牌图标库

#### 第7-8周：品牌化组件

**任务清单：**
- [ ] 创建品牌化卡片组件
- [ ] 创建品牌化按钮组件
- [ ] 创建品牌化统计卡片
- [ ] 更新所有页面使用品牌化组件

**交付物：**
- 品牌化组件库
- 更新后的页面

#### 第9-10周：成就系统

**任务清单：**
- [ ] 设计成就类型和条件
- [ ] 创建AchievementBadge组件
- [ ] 创建AchievementUnlock组件
- [ ] 实现成就检测逻辑
- [ ] 实现成就存储逻辑
- [ ] 添加成就页面

**交付物：**
- 成就系统
- 成就页面
- 成就通知系统

#### 第11-12周：优化和完善

**任务清单：**
- [ ] 添加品牌化动效
- [ ] 优化空状态设计
- [ ] 性能优化
- [ ] 用户测试
- [ ] Bug修复
- [ ] 文档更新

**交付物：**
- 完整的品牌化UI
- 用户测试报告
- 更新的文档

---

## 5. 验收标准

### 5.1 阶段一验收标准

#### 功能验收

- [ ] 所有页面正确显示图标
- [ ] 所有交互有明确的视觉反馈
- [ ] 加载状态显示骨架屏或加载动画
- [ ] 错误状态显示友好的错误提示
- [ ] 空状态显示引导性提示

#### 视觉验收

- [ ] 色彩系统统一，符合设计规范
- [ ] 排版系统统一，符合设计规范
- [ ] 间距和圆角统一，符合设计规范
- [ ] 阴影效果统一，符合设计规范
- [ ] 响应式布局在所有断点正常显示

#### 无障碍验收

- [ ] 所有交互元素有ARIA标签
- [ ] 焦点状态清晰可见
- [ ] 键盘导航正常工作
- [ ] 颜色对比度达到WCAG AA标准
- [ ] 屏幕阅读器可正常使用

#### 性能验收

- [ ] 首屏加载时间 < 2秒
- [ ] 交互响应时间 < 100ms
- [ ] 动画流畅度 > 60fps
- [ ] 无内存泄漏
- [ ] 无控制台错误

### 5.2 阶段二验收标准

#### 品牌验收

- [ ] Logo在所有页面正确显示
- [ ] 品牌色彩系统统一应用
- [ ] 品牌图标系统统一应用
- [ ] 品牌字体系统统一应用
- [ ] 品牌识别度明显提升

#### 功能验收

- [ ] 成就系统正常工作
- [ ] 成就解锁通知正常显示
- [ ] 成就页面正常显示
- [ ] 品牌化动效流畅
- [ ] 品牌化空状态友好

#### 用户验收

- [ ] 用户满意度调查 > 80%
- [ ] 用户留存率提升 > 20%
- [ ] 用户活跃度提升 > 15%
- [ ] 品牌识别度调查 > 70%
- [ ] 无重大Bug

---

## 6. 风险管理

### 6.1 技术风险

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| 图标加载性能问题 | 中 | 低 | 使用SVG格式，实现懒加载 |
| 动画性能问题 | 高 | 中 | 使用CSS动画，避免JavaScript动画 |
| 浏览器兼容性问题 | 中 | 中 | 使用CSS前缀，提供降级方案 |
| 响应式布局问题 | 中 | 中 | 充分测试各种设备和屏幕尺寸 |

### 6.2 设计风险

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| 用户不接受新设计 | 高 | 中 | A/B测试，渐进式推出 |
| 品牌识别度不足 | 中 | 中 | 强化品牌元素，持续优化 |
| 设计不一致 | 中 | 低 | 建立设计系统，组件化开发 |
| 无障碍支持不足 | 高 | 低 | 遵循WCAG标准，充分测试 |

### 6.3 进度风险

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| 开发周期延长 | 中 | 高 | 分阶段实施，优先级管理 |
| 资源不足 | 高 | 中 | 合理分配资源，必要时调整范围 |
| 需求变更 | 中 | 中 | 严格控制需求变更，评估影响 |

---

## 7. 成功指标

### 7.1 阶段一成功指标

- [ ] 用户体验评分提升 > 30%
- [ ] 任务完成率提升 > 20%
- [ ] 用户满意度 > 75%
- [ ] 无障碍评分达到WCAG AA
- [ ] 性能评分 > 90

### 7.2 阶段二成功指标

- [ ] 品牌识别度 > 70%
- [ ] 用户留存率提升 > 20%
- [ ] 用户活跃度提升 > 15%
- [ ] 成就系统参与度 > 60%
- [ ] 用户满意度 > 80%

---

## 8. 附录

### 8.1 参考资料

- [Heroicons](https://heroicons.com/) - 开源图标库
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/) - 无障碍标准
- [Inter Font](https://rsms.me/inter/) - 字体资源
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) - CSS变量文档

### 8.2 工具推荐

- **设计工具**：Figma, Sketch
- **图标工具**：Heroicons, Figma Icons
- **色彩工具**：Coolors, Adobe Color
- **无障碍工具**：axe DevTools, WAVE
- **性能工具**：Lighthouse, WebPageTest

### 8.3 联系方式

- **设计团队**：design@dotstore.com
- **开发团队**：dev@dotstore.com
- **产品团队**：product@dotstore.com

---

**文档变更日志**

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-02-07 | 初始版本，包含阶段一和阶段二设计 | UI设计团队 |

---

**文档审核**

- 审核人：技术负责人
- 审核日期：2026-02-07
- 审核状态：待审核
