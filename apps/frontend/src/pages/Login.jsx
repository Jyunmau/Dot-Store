import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
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

  // 登录
  const handleLogin = (e) => {
    e.preventDefault();
    
    if (!phone || !code) {
      setError('请输入手机号和验证码');
      return;
    }
    
    // 模拟登录
    setTimeout(() => {
      // 登录成功，跳转到会员中心
      navigate('/member/reservation');
    }, 1000);
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-title">天堂电影酒馆</h1>
        <h2 className="login-subtitle">登录</h2>
        
        {error && <div className="login-error">{error}</div>}
        
        <form onSubmit={handleLogin} className="login-form">
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
          
          <button type="submit" className="login-btn">登录</button>
        </form>
        
        <div className="login-footer">
          <p>还没有账号？<Link to="/register">立即注册</Link></p>
        </div>
      </div>
    </div>
  );
};

export default Login;
