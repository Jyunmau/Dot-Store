import React from 'react';

const Record = () => {
  return (
    <div className="record-page">
      <div className="page-header">
        <h1>记录</h1>
        <button className="new-record-btn">新记录</button>
      </div>
      
      <div className="filters-section">
        <div className="filter-group">
          <label>按日期</label>
          <select>
            <option>今天</option>
            <option>昨天</option>
            <option>最近7天</option>
            <option>自定义</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>按标签</label>
          <select>
            <option>全部</option>
            <option>堂食</option>
            <option>外卖</option>
            <option>活动</option>
            <option>临时</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>按状态</label>
          <select>
            <option>全部</option>
            <option>已完成</option>
            <option>待补充</option>
          </select>
        </div>
      </div>
      
      <div className="records-list">
        <div className="record-item">
          <div className="record-time">10:30</div>
          <div className="record-tags">
            <span className="tag">堂食</span>
            <span className="tag">活动</span>
          </div>
          <div className="record-desc">新品测试订单</div>
          <div className="record-status completed">已完成</div>
        </div>
        <div className="record-item">
          <div className="record-time">11:45</div>
          <div className="record-tags">
            <span className="tag">外卖</span>
          </div>
          <div className="record-desc">美团外卖订单</div>
          <div className="record-status pending">待补充</div>
        </div>
        <div className="record-item">
          <div className="record-time">13:20</div>
          <div className="record-tags">
            <span className="tag">堂食</span>
          </div>
          <div className="record-desc">常规订单</div>
          <div className="record-status completed">已完成</div>
        </div>
      </div>
    </div>
  );
};

export default Record;
