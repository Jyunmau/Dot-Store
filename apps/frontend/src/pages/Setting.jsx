import React from 'react';

const Setting = () => {
  return (
    <div className="setting-page">
      <h1>设置</h1>
      
      <div className="setting-section">
        <h2>基础信息</h2>
        <div className="setting-form">
          <div className="form-group">
            <label>店铺名称</label>
            <input type="text" placeholder="输入店铺名称" defaultValue="我的小店" />
          </div>
          <div className="form-group">
            <label>营业类型</label>
            <select defaultValue="餐饮">
              <option>餐饮</option>
              <option>咖啡</option>
              <option>其他</option>
            </select>
          </div>
        </div>
      </div>
      
      <div className="setting-section">
        <h2>标签管理</h2>
        <div className="tags-management">
          <div className="tags-list">
            <div className="tag-item">
              <div className="tag-info">
                <div className="tag-name">堂食</div>
                <div className="tag-description">堂食订单</div>
              </div>
              <div className="tag-actions">
                <button className="tag-action-btn active">启用</button>
                <button className="tag-action-btn">编辑</button>
              </div>
            </div>
            <div className="tag-item">
              <div className="tag-info">
                <div className="tag-name">外卖</div>
                <div className="tag-description">外卖订单</div>
              </div>
              <div className="tag-actions">
                <button className="tag-action-btn active">启用</button>
                <button className="tag-action-btn">编辑</button>
              </div>
            </div>
            <div className="tag-item">
              <div className="tag-info">
                <div className="tag-name">活动</div>
                <div className="tag-description">活动订单</div>
              </div>
              <div className="tag-actions">
                <button className="tag-action-btn active">启用</button>
                <button className="tag-action-btn">编辑</button>
              </div>
            </div>
          </div>
          <button className="add-tag-btn">添加标签</button>
        </div>
      </div>
      
      <div className="setting-section">
        <h2>显示配置</h2>
        <div className="toggle-settings">
          <div className="toggle-item">
            <div className="toggle-info">
              <div className="toggle-name">显示估算提示</div>
              <div className="toggle-description">在收入显示时显示估算标记</div>
            </div>
            <div className="toggle-switch">
              <input type="checkbox" id="show-estimate" defaultChecked />
              <label htmlFor="show-estimate"></label>
            </div>
          </div>
          <div className="toggle-item">
            <div className="toggle-info">
              <div className="toggle-name">提示未补全记录</div>
              <div className="toggle-description">在首页提示待补充的记录</div>
            </div>
            <div className="toggle-switch">
              <input type="checkbox" id="remind-pending" defaultChecked />
              <label htmlFor="remind-pending"></label>
            </div>
          </div>
        </div>
      </div>
      
      <div className="setting-actions">
        <button className="save-btn">保存设置</button>
      </div>
    </div>
  );
};

export default Setting;
