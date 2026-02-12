import React from 'react';

/**
 * 表单组组件
 * @param {string} label - 表单标签文本
 * @param {string} id - 表单控件ID，用于关联label和input
 * @param {string} helperText - 辅助文本
 * @param {boolean} error - 是否显示错误状态
 * @param {string} className - 自定义类名
 * @param {React.ReactNode} children - 表单控件
 * @returns {React.ReactElement}
 */
const FormGroup = ({ 
  label, 
  id, 
  helperText, 
  error = false, 
  className = '', 
  children 
}) => {
  // 组合所有类名
  const formGroupClass = `form-group ${error ? 'error' : ''} ${className}`.trim();
  
  return (
    <div className={formGroupClass}>
      {label && (
        <label htmlFor={id} className="form-label">
          {label}
        </label>
      )}
      {children}
      {(helperText || error) && (
        <div className="helper-text">
          {helperText}
        </div>
      )}
    </div>
  );
};

export default FormGroup;