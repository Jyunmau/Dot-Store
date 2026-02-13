import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const AccountSettings = () => {
  const [accountInfo, setAccountInfo] = useState({
    shopName: '天堂电影酒馆',
    contactPerson: '张三',
    phone: '13800138000',
    email: 'info@example.com',
    address: '北京市朝阳区望京SOHO T3',
    businessHours: '10:00 - 22:00'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  // 更新账户信息
  const updateAccountInfo = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      // 模拟更新，实际应该调用API
      console.log('更新账户信息:', accountInfo);
      setSuccess(true);
      // 3秒后清除成功提示
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error('更新账户信息失败:', err);
      setError('更新账户信息失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  // 处理表单输入变化
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setAccountInfo(prev => ({ ...prev, [name]: value }));
  };
  
  return (
    <div className="account-settings-page">
      <div className="page-header">
        <h1>账户设置</h1>
      </div>
      
      {/* 账户信息表单 */}
      <div className="card level1 account-info-form">
        <h2>基本信息</h2>
        {success && (
          <div className="success-message">
            账户信息更新成功！
          </div>
        )}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        <form onSubmit={updateAccountInfo}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="shopName">店铺名称</label>
              <input
                type="text"
                id="shopName"
                name="shopName"
                value={accountInfo.shopName}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="contactPerson">联系人</label>
              <input
                type="text"
                id="contactPerson"
                name="contactPerson"
                value={accountInfo.contactPerson}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="phone">联系电话</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={accountInfo.phone}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">电子邮箱</label>
              <input
                type="email"
                id="email"
                name="email"
                value={accountInfo.email}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="address">店铺地址</label>
            <textarea
              id="address"
              name="address"
              value={accountInfo.address}
              onChange={handleInputChange}
              rows="3"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="businessHours">营业时间</label>
            <input
              type="text"
              id="businessHours"
              name="businessHours"
              value={accountInfo.businessHours}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="primary" disabled={loading}>
              {loading ? '保存中...' : '保存设置'}
            </button>
          </div>
        </form>
      </div>
      
      {/* 密码设置 */}
      <div className="card level1 password-settings-form">
        <h2>密码设置</h2>
        <form onSubmit={(e) => {
          e.preventDefault();
          console.log('更新密码');
        }}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="currentPassword">当前密码</label>
              <input
                type="password"
                id="currentPassword"
                name="currentPassword"
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="newPassword">新密码</label>
              <input
                type="password"
                id="newPassword"
                name="newPassword"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="confirmPassword">确认新密码</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                required
              />
            </div>
          </div>
          <div className="form-actions">
            <button type="submit" className="primary">修改密码</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AccountSettings;