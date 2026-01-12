import React from 'react';

const Report = () => {
  return (
    <div className="report-page">
      <div className="page-header">
        <h1>报表</h1>
        <div className="time-range-selector">
          <button className="range-btn">7天</button>
          <button className="range-btn active">30天</button>
          <button className="range-btn">自定义</button>
        </div>
      </div>
      
      <div className="core-metrics">
        <div className="metric-card">
          <h3>总收入</h3>
          <p className="metric-value income">¥12,345.67</p>
        </div>
        <div className="metric-card">
          <h3>总支出</h3>
          <p className="metric-value expense">¥4,567.89</p>
        </div>
        <div className="metric-card highlight">
          <h3>净利润</h3>
          <p className="metric-value profit">¥7,777.78</p>
        </div>
      </div>
      
      <div className="trend-section">
        <h2>盈亏变化</h2>
        <div className="trend-chart">
          {/* 简单的折线图占位 */}
          <div className="chart-placeholder">
            <div className="chart-line"></div>
            <div className="chart-axis">
              <div className="x-axis">日期</div>
              <div className="y-axis">金额</div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="category-analysis">
        <div className="analysis-group">
          <h2>按标签分析</h2>
          <div className="category-list">
            <div className="category-item">
              <div className="category-info">
                <div className="category-name">堂食</div>
                <div className="category-percent">65%</div>
              </div>
              <div className="category-bar">
                <div className="bar-fill" style={{ width: '65%' }}></div>
              </div>
              <div className="category-amount">¥8,024.69</div>
            </div>
            <div className="category-item">
              <div className="category-info">
                <div className="category-name">外卖</div>
                <div className="category-percent">25%</div>
              </div>
              <div className="category-bar">
                <div className="bar-fill" style={{ width: '25%' }}></div>
              </div>
              <div className="category-amount">¥3,086.42</div>
            </div>
            <div className="category-item">
              <div className="category-info">
                <div className="category-name">活动</div>
                <div className="category-percent">10%</div>
              </div>
              <div className="category-bar">
                <div className="bar-fill" style={{ width: '10%' }}></div>
              </div>
              <div className="category-amount">¥1,234.56</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Report;
