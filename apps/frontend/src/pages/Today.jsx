import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
  const [selectedDate, setSelectedDate] = useState(new Date());
  const navigate = useNavigate();
  
  // 获取数据
  const fetchData = async () => {
    try {
      setLoading(true);
      
      // 模拟 shop_id，实际应该从登录状态或上下文获取
      const shopId = 1;
      const date = selectedDate.toISOString().split('T')[0];
      
      // 获取汇总数据
      const summaryData = await api.report.summary(shopId, date);
      setSummary({
        total_income: summaryData.total_income,
        total_expense: summaryData.total_expense,
        net_profit: summaryData.net_profit
      });
      
      // 获取记录列表
      const recordsData = await api.order.list(shopId);
      setRecords(recordsData);
      
      setError(null);
    } catch (err) {
      console.error('获取数据失败:', err);
      setError('获取数据失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  // 切换日期
  const changeDate = (days) => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + days);
    setSelectedDate(newDate);
  };
  
  // 设置为今天
  const setToToday = () => {
    setSelectedDate(new Date());
  };
  
  // 记录订单
  const recordOrder = () => {
    navigate('/record', { state: { type: 'order' } });
  };
  
  // 记录收入
  const recordIncome = () => {
    navigate('/record', { state: { type: 'income' } });
  };
  
  // 记录支出
  const recordExpense = () => {
    navigate('/record', { state: { type: 'expense' } });
  };
  
  // 查看记录详情
  const viewRecordDetail = (recordId) => {
    // 这里可以导航到记录详情页或显示详情模态框
    console.log('查看记录详情:', recordId);
  };
  
  useEffect(() => {
    fetchData();
  }, [selectedDate]);
  
  return (
    <div className="today-page">
      <div className="page-header">
        <h1>今日盈亏概览</h1>
      </div>
      
      {/* 日期选择器 */}
      <div className="date-section card level1">
        <div className="date-selector">
          <button className="secondary" onClick={() => changeDate(-1)}>昨天</button>
          <h2 className="selected-date">{selectedDate.toISOString().split('T')[0]}</h2>
          <button className="secondary" onClick={() => changeDate(1)}>明天</button>
        </div>
        <button className="primary small" onClick={setToToday}>今天</button>
      </div>
      
      {loading ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="loading"></div>
        </div>
      ) : error ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="error" style={{ color: '#F5222D', textAlign: 'center' }}>
            <p>{error}</p>
            <button className="primary" onClick={fetchData} style={{ marginTop: '16px' }}>重试</button>
          </div>
        </div>
      ) : (
        <>
          {/* 统计概览卡片 */}
          <div className="summary-section">
            <h3>今日关键指标</h3>
            <div className="summary-cards-container">
              <div className="summary-card card level1" onClick={() => console.log('查看今日收入详情')}>
                <h4>今日收入</h4>
                <p className="amount income">¥{summary.total_income.toFixed(2)}</p>
                <p className="estimate" style={{ fontSize: '12px', color: '#8C8C8C' }}>估算值</p>
              </div>
              <div className="summary-card card level1" onClick={() => console.log('查看今日支出详情')}>
                <h4>今日支出</h4>
                <p className="amount expense">¥{summary.total_expense.toFixed(2)}</p>
              </div>
              <div className="summary-card card level1 highlight" onClick={() => console.log('查看今日盈亏详情')}>
                <h4>今日盈亏</h4>
                <p className="amount profit">¥{summary.net_profit.toFixed(2)}</p>
              </div>
            </div>
          </div>
          
          {/* 快速记录按钮 */}
          <div className="quick-actions-section">
            <h3>快速记录</h3>
            <div className="quick-actions">
              <button className="card level2 quick-action-btn" onClick={recordOrder}>
                <h4>记录订单</h4>
              </button>
              <button className="card level2 quick-action-btn" onClick={recordIncome}>
                <h4>记录收入</h4>
              </button>
              <button className="card level2 quick-action-btn" onClick={recordExpense}>
                <h4>记录支出</h4>
              </button>
            </div>
          </div>
          
          {/* 今日记录列表 */}
          <div className="records-section">
            <h3>今日记录</h3>
            <div className="records-list card level1">
              {records.length > 0 ? (
                records.map((record) => (
                  <div 
                    key={record.id} 
                    className="record-item" 
                    onClick={() => viewRecordDetail(record.id)}
                  >
                    <div className="record-content">
                      <h4>{record.metadata?.note || '无描述'}</h4>
                      <p className="record-time" style={{ fontSize: '12px', color: '#8C8C8C' }}>
                        {new Date(record.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                    <div className="record-amount">
                      <p className={`amount ${record.type === 'income' ? 'income' : 'expense'}`}>
                        {record.type === 'income' ? '+' : '-'}{'¥'}{Math.abs(record.amount).toFixed(2)}
                      </p>
                    </div>
                    <div className={`record-status ${record.status === 'recorded' ? 'completed' : 'pending'}`}>
                      {record.status === 'recorded' ? '已完成' : '待补充'}
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-records" style={{ padding: '48px', textAlign: 'center', color: '#8C8C8C' }}>
                  <p>今日暂无记录</p>
                  <p style={{ fontSize: '12px', marginTop: '8px' }}>点击上方按钮开始记录</p>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Today;
