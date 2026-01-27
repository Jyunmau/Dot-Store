import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Report = () => {
  const [dateRange, setDateRange] = useState('today'); // today, week, month, custom
  const [customDates, setCustomDates] = useState({
    startDate: '',
    endDate: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [incomeStructure, setIncomeStructure] = useState([]);
  const [costStructure, setCostStructure] = useState([]);

  // 获取报表数据
  const fetchReportData = async () => {
    try {
      setLoading(true);
      
      // 模拟 shop_id，实际应该从登录状态或上下文获取
      const shopId = 1;
      
      // 准备日期参数
      const dateParams = {
        date_range: dateRange,
        start_date: customDates.startDate || null,
        end_date: customDates.endDate || null
      };
      
      // 获取收入结构数据
      const incomeStructureData = await api.report.incomeStructure(shopId, dateParams);
      // 转换数据格式
      const incomeItems = Object.entries(incomeStructureData.income_structure).map(([account_id, amount]) => {
        return { name: `账户${account_id}`, amount: amount || 0, percentage: 0 };
      });
      // 计算百分比
      const totalIncome = incomeItems.reduce((sum, item) => sum + item.amount, 0);
      const formattedIncomeStructure = incomeItems.map(item => {
        return {
          ...item,
          percentage: totalIncome > 0 ? Math.round((item.amount / totalIncome) * 100) : 0
        };
      });
      setIncomeStructure(formattedIncomeStructure);
      
      // 获取成本结构数据
      const expenseStructureData = await api.report.expenseStructure(shopId, dateParams);
      // 转换数据格式
      const costItems = Object.entries(expenseStructureData.expense_structure).map(([account_id, amount]) => {
        return { name: `账户${account_id}`, amount: amount || 0, percentage: 0 };
      });
      // 计算百分比
      const totalCost = costItems.reduce((sum, item) => sum + item.amount, 0);
      const formattedCostStructure = costItems.map(item => {
        return {
          ...item,
          percentage: totalCost > 0 ? Math.round((item.amount / totalCost) * 100) : 0
        };
      });
      setCostStructure(formattedCostStructure);
      
      setError(null);
    } catch (err) {
      console.error('获取报表数据失败:', err);
      setError('获取报表数据失败，请稍后重试');
      // 使用模拟数据作为备份
      setIncomeStructure([
        { name: '餐饮订单', amount: 1234, percentage: 60 },
        { name: '外卖订单', amount: 567, percentage: 28 },
        { name: '其他收入', amount: 245, percentage: 12 }
      ]);
      
      setCostStructure([
        { name: '食材采购', amount: 567, percentage: 50 },
        { name: '房租水电', amount: 234, percentage: 21 },
        { name: '人员工资', amount: 123, percentage: 11 },
        { name: '其他成本', amount: 200, percentage: 18 }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 切换日期范围
  const handleDateRangeChange = (range) => {
    setDateRange(range);
    fetchReportData();
  };

  // 自定义日期变化处理
  const handleCustomDateChange = (e) => {
    const { name, value } = e.target;
    setCustomDates(prev => ({ ...prev, [name]: value }));
  };

  // 应用自定义日期范围
  const applyCustomDateRange = () => {
    if (customDates.startDate && customDates.endDate) {
      fetchReportData();
    }
  };

  // 导出报表数据
  const exportReport = () => {
    // 实现导出功能
    console.log('导出报表数据');
  };

  useEffect(() => {
    fetchReportData();
  }, [dateRange, customDates.startDate, customDates.endDate]);

  return (
    <div className="report-page">
      <div className="page-header">
        <h1>报表</h1>
        <button className="primary" onClick={exportReport}>导出报表</button>
      </div>
      
      {/* 日期范围选择 */}
      <div className="date-range-section card level1">
        <div className="date-range-buttons">
          <button 
            className={`range-btn ${dateRange === 'today' ? 'active' : ''}`}
            onClick={() => handleDateRangeChange('today')}
          >
            今日
          </button>
          <button 
            className={`range-btn ${dateRange === 'week' ? 'active' : ''}`}
            onClick={() => handleDateRangeChange('week')}
          >
            本周
          </button>
          <button 
            className={`range-btn ${dateRange === 'month' ? 'active' : ''}`}
            onClick={() => handleDateRangeChange('month')}
          >
            本月
          </button>
          <button 
            className={`range-btn ${dateRange === 'custom' ? 'active' : ''}`}
            onClick={() => handleDateRangeChange('custom')}
          >
            自定义
          </button>
        </div>
        
        {/* 自定义日期范围输入 */}
        {dateRange === 'custom' && (
          <div className="custom-date-range">
            <input
              type="date"
              name="startDate"
              value={customDates.startDate}
              onChange={handleCustomDateChange}
              placeholder="开始日期"
            />
            <span className="date-separator">至</span>
            <input
              type="date"
              name="endDate"
              value={customDates.endDate}
              onChange={handleCustomDateChange}
              placeholder="结束日期"
            />
            <button className="primary small" onClick={applyCustomDateRange}>应用</button>
          </div>
        )}
      </div>
      
      {loading ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="loading"></div>
        </div>
      ) : error ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="error" style={{ color: '#F5222D', textAlign: 'center' }}>
            <p>{error}</p>
            <button className="primary" onClick={fetchReportData} style={{ marginTop: '16px' }}>重试</button>
          </div>
        </div>
      ) : (
        <>
          {/* 收入结构报表 */}
          <div className="report-section">
            <h2>收入结构</h2>
            <div className="report-card card level1">
              {/* 收入结构饼图（占位） */}
              <div className="chart-container">
                <div className="pie-chart-placeholder">
                  {/* 简单的饼图模拟 */}
                  <div className="pie-chart">
                    {incomeStructure.map((item, index) => (
                      <div 
                        key={index} 
                        className="pie-slice"
                        style={{
                          background: `hsl(${index * 120}, 70%, 60%)`,
                          clipPath: `polygon(50% 50%, 50% 0%, ${50 + 50 * Math.cos(2 * Math.PI * (item.percentage / 100))}% ${50 - 50 * Math.sin(2 * Math.PI * (item.percentage / 100))}%)`
                        }}
                      ></div>
                    ))}
                  </div>
                </div>
              </div>
              
              {/* 收入结构明细 */}
              <div className="structure-details">
                {incomeStructure.map((item, index) => (
                  <div key={index} className="structure-item">
                    <div className="item-info">
                      <span className="item-name">{item.name}</span>
                      <span className="item-percentage">{item.percentage}%</span>
                    </div>
                    <div className="item-amount">¥{item.amount.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          {/* 成本结构报表 */}
          <div className="report-section">
            <h2>成本结构</h2>
            <div className="report-card card level1">
              {/* 成本结构柱状图（占位） */}
              <div className="chart-container">
                <div className="bar-chart-placeholder">
                  {/* 简单的柱状图模拟 */}
                  <div className="bar-chart">
                    {costStructure.map((item, index) => (
                      <div key={index} className="bar-item">
                        <div className="bar-label">{item.name}</div>
                        <div className="bar-container">
                          <div 
                            className="bar-fill"
                            style={{ 
                              height: `${item.percentage}%`,
                              background: `hsl(${index * 90}, 70%, 60%)`
                            }}
                          ></div>
                        </div>
                        <div className="bar-value">¥{item.amount.toFixed(2)}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              
              {/* 成本结构明细 */}
              <div className="structure-details">
                {costStructure.map((item, index) => (
                  <div key={index} className="structure-item">
                    <div className="item-info">
                      <span className="item-name">{item.name}</span>
                      <span className="item-percentage">{item.percentage}%</span>
                    </div>
                    <div className="item-amount">¥{item.amount.toFixed(2)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Report;
