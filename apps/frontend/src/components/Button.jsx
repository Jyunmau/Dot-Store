import React from 'react';

/**
 * 按钮组件
 * @param {string} type - 按钮类型：primary, secondary, danger, text
 * @param {string} size - 按钮尺寸：small, medium, large
 * @param {boolean} disabled - 是否禁用
 * @param {function} onClick - 点击事件处理函数
 * @param {string} className - 自定义类名
 * @param {React.ReactNode} children - 按钮内容
 * @returns {React.ReactElement}
 */
const Button = ({ 
  type = 'primary', 
  size = 'medium', 
  disabled = false, 
  onClick, 
  className = '', 
  children, 
  ...props 
}) => {
  // 按钮类型类名
  const typeClass = {
    primary: 'primary',
    secondary: 'secondary',
    danger: 'danger',
    text: 'text'
  }[type] || 'primary';
  
  // 按钮尺寸类名
  const sizeClass = {
    small: 'small',
    medium: '',
    large: 'large'
  }[size] || '';
  
  // 组合所有类名
  const btnClass = `button ${typeClass} ${sizeClass} ${disabled ? 'disabled' : ''} ${className}`.trim();
  
  return (
    <button
      className={btnClass}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;