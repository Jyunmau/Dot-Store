import React from 'react';

/**
 * 卡片组件
 * @param {string} level - 卡片阴影级别：1, 2, 3
 * @param {boolean} highlight - 是否高亮
 * @param {boolean} border - 是否显示边框
 * @param {string} className - 自定义类名
 * @param {React.ReactNode} children - 卡片内容
 * @returns {React.ReactElement}
 */
const Card = ({ 
  level = 1, 
  highlight = false, 
  border = false, 
  className = '', 
  children 
}) => {
  // 卡片阴影级别类名
  const levelClass = level >= 1 && level <= 3 ? `level${level}` : 'level1';
  
  // 组合所有类名
  const cardClass = `card ${levelClass} ${highlight ? 'highlight' : ''} ${border ? 'border' : ''} ${className}`.trim();
  
  return (
    <div className={cardClass}>
      {children}
    </div>
  );
};

export default Card;