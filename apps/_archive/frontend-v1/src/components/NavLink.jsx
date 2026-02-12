import React from 'react';
import { NavLink as RouterNavLink } from 'react-router-dom';

/**
 * 导航链接组件
 * @param {string} to - 目标路由路径
 * @param {boolean} exact - 是否精确匹配
 * @param {boolean} end - 是否匹配到末尾
 * @param {string} className - 自定义类名
 * @param {React.ReactNode} children - 链接内容
 * @returns {React.ReactElement}
 */
const NavLink = ({ 
  to, 
  exact = false, 
  end = false, 
  className = '', 
  children, 
  ...props 
}) => {
  return (
    <RouterNavLink
      to={to}
      exact={exact}
      end={end}
      className={({ isActive }) => {
        return `nav-link ${isActive ? 'active' : ''} ${className}`.trim();
      }}
      {...props}
    >
      {children}
    </RouterNavLink>
  );
};

export default NavLink;