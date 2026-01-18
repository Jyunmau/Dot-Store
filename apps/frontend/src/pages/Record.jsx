import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Record = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    date: '今天',
    tag: '全部',
    status: '全部'
  });

  // 加载订单记录
  useEffect(() => {
    const fetchRecords = async () => {
      try {
        setLoading(true);
        // 这里使用模拟的shop_id=1，实际应用中应该从登录状态获取
        const response = await api.order.list(1);
        setRecords(response);
      } catch (error) {
        console.error('获取订单记录失败:', error);
        // 为了演示，使用模拟数据
        setRecords([
          {
            id: 1,
            created_at: new Date().toISOString(),
            tags: ['堂食', '活动'],
            metadata: { note: '新品测试订单' },
            status: 'completed'
          },
          {
            id: 2,
            created_at: new Date().toISOString(),
            tags: ['外卖'],
            metadata: { note: '美团外卖订单' },
            status: 'recorded'
          },
          {
            id: 3,
            created_at: new Date().toISOString(),
            tags: ['堂食'],
            metadata: { note: '常规订单' },
            status: 'completed'
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();
  }, [filters]);

  // 创建新记录
  const handleNewRecord = async () => {
    try {
      const newRecord = {
        shop_id: 1,
        amount_estimate: 0,
        tags: [],
        metadata: {}
      };
      const response = await api.order.create(newRecord);
      console.log('新记录创建成功:', response);
      // 重新加载记录列表
      const updatedRecords = await api.order.list(1);
      setRecords(updatedRecords);
    } catch (error) {
      console.error('创建新记录失败:', error);
      alert('创建新记录失败，请稍后重试');
    }
  };

  // 格式化时间
  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="record-page">
      <div className="page-header">
        <h1>记录</h1>
        <button className="new-record-btn" onClick={handleNewRecord}>
          新记录
        </button>
      </div>
      
      <div className="filters-section">
        <div className="filter-group">
          <label>按日期</label>
          <select 
            value={filters.date}
            onChange={(e) => setFilters({...filters, date: e.target.value})}
          >
            <option>今天</option>
            <option>昨天</option>
            <option>最近7天</option>
            <option>自定义</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>按标签</label>
          <select 
            value={filters.tag}
            onChange={(e) => setFilters({...filters, tag: e.target.value})}
          >
            <option>全部</option>
            <option>堂食</option>
            <option>外卖</option>
            <option>活动</option>
            <option>临时</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>按状态</label>
          <select 
            value={filters.status}
            onChange={(e) => setFilters({...filters, status: e.target.value})}
          >
            <option>全部</option>
            <option>已完成</option>
            <option>待补充</option>
          </select>
        </div>
      </div>
      
      {loading ? (
        <div className="loading">加载中...</div>
      ) : (
        <div className="records-list">
          {records.map(record => (
            <div key={record.id} className="record-item">
              <div className="record-time">{formatTime(record.created_at)}</div>
              <div className="record-tags">
                {record.tags && record.tags.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
              <div className="record-desc">{record.metadata?.note || '无描述'}</div>
              <div className={`record-status ${record.status === 'completed' ? 'completed' : 'pending'}`}>
                {record.status === 'completed' ? '已完成' : '待补充'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Record;
