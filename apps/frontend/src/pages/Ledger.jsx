import React from 'react';

const Ledger = () => {
  return (
    <div className="ledger-page">
      <div className="page-header">
        <h1>账本</h1>
        <div className="period-selector">
          <button className="period-btn active">今天</button>
          <button className="period-btn">本周</button>
          <button className="period-btn">自定义</button>
        </div>
      </div>
      
      <div className="ledger-accounts">
        <div className="account-group">
          <h2>收入类</h2>
          <div className="accounts-list">
            <div className="account-item">
              <div className="account-info">
                <div className="account-name">堂食收入</div>
                <div className="account-code">1001</div>
              </div>
              <div className="account-balance income">¥890.00</div>
            </div>
            <div className="account-item">
              <div className="account-info">
                <div className="account-name">外卖收入</div>
                <div className="account-code">1002</div>
              </div>
              <div className="account-balance income">¥344.56</div>
            </div>
          </div>
        </div>
        
        <div className="account-group">
          <h2>支出类</h2>
          <div className="accounts-list">
            <div className="account-item">
              <div className="account-info">
                <div className="account-name">食材成本</div>
                <div className="account-code">2001</div>
              </div>
              <div className="account-balance expense">¥234.56</div>
            </div>
            <div className="account-item">
              <div className="account-info">
                <div className="account-name">房租水电</div>
                <div className="account-code">2002</div>
              </div>
              <div className="account-balance expense">¥222.22</div>
            </div>
          </div>
        </div>
        
        <div className="account-group">
          <h2>调整类</h2>
          <div className="accounts-list">
            <div className="account-item">
              <div className="account-info">
                <div className="account-name">手工调整</div>
                <div className="account-code">3001</div>
              </div>
              <div className="account-balance">¥0.00</div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="entries-section">
        <h2>明细</h2>
        <div className="entries-list">
          <div className="entry-item">
            <div className="entry-time">10:30</div>
            <div className="entry-amount income">+¥58.00</div>
            <div className="entry-source">自动</div>
            <div className="entry-desc">早餐销售 #1001</div>
          </div>
          <div className="entry-item">
            <div className="entry-time">11:45</div>
            <div className="entry-amount expense">-¥22.00</div>
            <div className="entry-source">自动</div>
            <div className="entry-desc">食材采购 #2001</div>
          </div>
        </div>
        
        <button className="add-entry-btn">手工调整</button>
      </div>
    </div>
  );
};

export default Ledger;
