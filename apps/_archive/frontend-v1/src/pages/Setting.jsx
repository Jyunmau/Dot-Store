import React from 'react';
import { useNavigate, Outlet } from 'react-router-dom';

const Setting = () => {
  const navigate = useNavigate();

  // 设置选项列表
  const settingsOptions = [
    {
      id: 'account-categories',
      name: '账目分类管理',
      description: '管理收入和支出的分类',
      icon: '📋'
    },
    {
      id: 'tags',
      name: '标签管理',
      description: '管理记录的标签',
      icon: '🏷️'
    },
    {
      id: 'business-types',
      name: '业务类型管理',
      description: '管理业务类型设置',
      icon: '💼'
    },
    {
      id: 'account-settings',
      name: '账户设置',
      description: '管理账户基本信息',
      icon: '👤'
    },
    {
      id: 'about',
      name: '关于',
      description: '关于Dot-Store应用',
      icon: 'ℹ️'
    }
  ];

  // 处理设置选项点击
  const handleSettingClick = (optionId) => {
    // 导航到相应的设置页面
    navigate(`/setting/${optionId}`);
  };

  return (
    <div className="setting-page">
      <div className="page-header">
        <h1>设置</h1>
      </div>
      
      {/* 设置选项列表 */}
      <div className="settings-options">
        {settingsOptions.map((option) => (
          <div 
            key={option.id} 
            className="setting-option card level1"
            onClick={() => handleSettingClick(option.id)}
          >
            <div className="setting-option-icon">{option.icon}</div>
            <div className="setting-option-info">
              <h3 className="setting-option-name">{option.name}</h3>
              <p className="setting-option-description">{option.description}</p>
            </div>
            <div className="setting-option-arrow">›</div>
          </div>
        ))}
      </div>
      
      {/* 子页面内容区域 */}
      <Outlet />
    </div>
  );
};

export default Setting;
