import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [name, setName] = useState('');
  const [isSendingCode, setIsSendingCode] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // 发送验证码
  const handleSendCode = () => {
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      setError('请输入有效的手机号');
      return;
    }
    
    setIsSendingCode(true);
    setCountdown(60);
    setError(null);
    
    // 模拟发送验证码
    setTimeout(() => {
      setIsSendingCode(false);
      alert('验证码已发送至您的手机');
    }, 1000);
    
    // 倒计时
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  // 注册
  const handleRegister = (e) => {
    e.preventDefault();
    
    if (!phone || !code || !name) {
      setError('请填写完整的注册信息');
      return;
    }
    
    // 模拟注册
    setTimeout(() => {
      // 注册成功，跳转到登录页面
      alert('注册成功，请登录');
      navigate('/login');
    }, 1000);
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h1 className="register-title">天堂电影酒馆</h1>
        <h2 className="register-subtitle">注册</h2>
        
        {error && <div className="register-error">{error}</div>}
        
        <form onSubmit={handleRegister} className="register-form">
          <div className="form-group">
            <label htmlFor="name">姓名</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="请输入您的姓名"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="phone">手机号</label>
            <input
              type="tel"
              id="phone"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="请输入手机号"
              required
            />
          </div>
          
          <div className="form-group">
            <div className="code-input-group">
              <div style={{ flex: 1 }}>
                <label htmlFor="code">验证码</label>
                <input
                  type="text"
                  id="code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="请输入验证码"
                  required
                />
              </div>
              <button
                type="button"
                className="send-code-btn"
                onClick={handleSendCode}
                disabled={isSendingCode || countdown > 0}
              >
                {isSendingCode ? '发送中...' : countdown > 0 ? `${countdown}s后重发` : '获取验证码'}
              </button>
            </div>
          </div>
          
          <button type="submit" className="register-btn">注册</button>
        </form>
        
        <div className="register-footer">
          <p>已有账号？<Link to="/login">立即登录</Link></p>
        </div>
      </div>
    </div>
  );
};

export default Register;
