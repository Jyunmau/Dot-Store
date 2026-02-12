import React from 'react';

const AdminLogin = () => {
  return (
    <div className="admin-login-page">
      <div className="login-container">
        <h1>管理员登录</h1>
        <form className="login-form">
          <div className="form-group">
            <label>用户名</label>
            <input type="text" placeholder="请输入用户名" />
          </div>
          <div className="form-group">
            <label>密码</label>
            <input type="password" placeholder="请输入密码" />
          </div>
          <button type="submit" className="login-btn">登录</button>
        </form>
      </div>
    </div>
  );
};

export default AdminLogin;