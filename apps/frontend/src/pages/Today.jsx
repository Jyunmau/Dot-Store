import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Today = () => {
  const [summary, setSummary] = useState({
    total_income: 0,
    total_expense: 0,
    net_profit: 0
  });
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // 获取今日数据
  const fetchTodayData = async () => {
    try {
      setLoading(true);
      
      // 模拟 shop_id，实际应该从登录状态或上下文获取
      const shopId = 1;
      const today = new Date().toISOString().split('T')[0];
      
      // 获取今日汇总数据
      const summaryData = await api.report.summary(shopId, today);
      setSummary({
        total_income: summaryData.total_income,
        total_expense: summaryData.total_expense,
        net_profit: summaryData.net_profit
      });
      
      // 获取今日记录列表
      const recordsData = await api.order.list(shopId);
      setRecords(recordsData);
      
      setError(null);
    } catch (err) {
      console.error('获取今日数据失败:', err);
      setError('获取数据失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchTodayData();
  }, []);
  
  return (
    <div className="today-page">
      <h1>今日</h1>
      <div className="date-section">
        <h2>{new Date().toISOString().split('T')[0]}</h2>
        <div className="date-nav">
          <button className="secondary">昨天</button>
          <button className="secondary">明天</button>
        </div>
      </div>
      
      {loading ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="loading"></div>
        </div>
      ) : error ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="error" style={{ color: '#F5222D', textAlign: 'center' }}>
            <p>{error}</p>
            <button className="primary" onClick={fetchTodayData} style={{ marginTop: '16px' }}>重试</button>
          </div>
        </div>
      ) : (
        <>
          <div className="summary-section summary-cards-container">
            <div className="summary-card card level1">
              <h3>今日收入</h3>
              <p className="amount income">¥{summary.total_income.toFixed(2)}</p>
              <p className="estimate" style={{ fontSize: '12px', color: '#8C8C8C' }}>估算值</p>
            </div>
            <div className="summary-card card level1">
              <h3>今日支出</h3>
              <p className="amount expense">¥{summary.total_expense.toFixed(2)}</p>
            </div>
            <div className="summary-card card level1 highlight">
              <h3>今日盈亏</h3>
              <p className="amount profit">¥{summary.net_profit.toFixed(2)}</p>
            </div>
          </div>
          
          <div className="records-section">
            <h3>今日发生了什么</h3>
            <div className="records-list card level1">
              {records.length > 0 ? (
                records.map((record) => (
                  <div key={record.id} className="record-item">
                    <div className="record-tags">
                      {record.tags && record.tags.map((tag, index) => (
                        <span key={index} className="tag">{tag}</span>
                      ))}
                    </div>
                    <div className="record-content">
                      <p className="record-desc">{record.metadata?.note || '无描述'}</p>
                      <p className="record-time" style={{ fontSize: '12px', color: '#8C8C8C' }}>{new Date(record.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                    </div>
                    <div className={`record-status ${record.status === 'recorded' ? 'completed' : 'pending'}`}>
                      {record.status === 'recorded' ? '已完成' : '待补充'}
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-records" style={{ padding: '48px', textAlign: 'center', color: '#8C8C8C' }}>
                  <p>今日暂无记录</p>
                  <p style={{ fontSize: '12px', marginTop: '8px' }}>点击右下角按钮开始记录</p>
                </div>
              )}
            </div>
          </div>
        </>
      )}
      
      <div className="actions-section">
        <button className="action-btn primary">记一笔</button>
        <button className="action-btn secondary">调整账目</button>
      </div>
    </div>
  );
};

export default Today;
