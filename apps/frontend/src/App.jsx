import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import './App.css';

// 导入页面组件
import Today from './pages/Today';
import Record from './pages/Record';
import Ledger from './pages/Ledger';
import Report from './pages/Report';
import Setting from './pages/Setting';
// 会员端页面组件
import Login from './pages/Login';
import Register from './pages/Register';
import Reservation from './pages/Reservation';
import MemberCenter from './pages/MemberCenter';
import OrderHistory from './pages/OrderHistory';
import Wallet from './pages/Wallet';
// 管理员端页面组件
import AdminLogin from './pages/admin/Login';
import AdminDashboard from './pages/admin/Dashboard';
import SeatManagement from './pages/admin/SeatManagement';
import ReservationManagement from './pages/admin/ReservationManagement';
import MemberManagement from './pages/admin/MemberManagement';
import CashbackConfig from './pages/admin/CashbackConfig';


function App() {
  return (
    <Router>
      <div className="App">
        {/* 主路由 */}
        <Routes>
          {/* 会员端公开路由 */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* 管理员端路由 */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/*" element={
            <div className="admin-layout">
              <nav className="admin-nav-bar">
                <h1 className="admin-title">Dot-Store 管理后台</h1>
              </nav>
              <div className="admin-container">
                <aside className="admin-side-nav">
                  <NavLink to="/admin" className={({ isActive }) => isActive ? 'admin-nav-link active' : 'admin-nav-link'} end>
                    仪表盘
                  </NavLink>
                  <NavLink to="/admin/seat-management" className={({ isActive }) => isActive ? 'admin-nav-link active' : 'admin-nav-link'}>
                    座位管理
                  </NavLink>
                  <NavLink to="/admin/reservation-management" className={({ isActive }) => isActive ? 'admin-nav-link active' : 'admin-nav-link'}>
                    预订管理
                  </NavLink>
                  <NavLink to="/admin/member-management" className={({ isActive }) => isActive ? 'admin-nav-link active' : 'admin-nav-link'}>
                    会员管理
                  </NavLink>
                  <NavLink to="/admin/cashback-config" className={({ isActive }) => isActive ? 'admin-nav-link active' : 'admin-nav-link'}>
                    返现配置
                  </NavLink>
                </aside>
                <main className="admin-main-content">
                  <Routes>
                    <Route path="/" element={<AdminDashboard />} />
                    <Route path="/seat-management" element={<SeatManagement />} />
                    <Route path="/reservation-management" element={<ReservationManagement />} />
                    <Route path="/member-management" element={<MemberManagement />} />
                    <Route path="/cashback-config" element={<CashbackConfig />} />
                  </Routes>
                </main>
              </div>
            </div>
          } />
          
          {/* 会员端路由 */}
          <Route path="/member/*" element={
            <div className="member-layout">
              <nav className="member-nav-bar">
                <h1 className="member-title">天堂电影酒馆</h1>
              </nav>
              <div className="member-container">
                <aside className="member-side-nav">
                  <NavLink to="/member/reservation" className={({ isActive }) => isActive ? 'member-nav-link active' : 'member-nav-link'}>
                    酒台预订
                  </NavLink>
                  <NavLink to="/member/order-history" className={({ isActive }) => isActive ? 'member-nav-link active' : 'member-nav-link'}>
                    订单历史
                  </NavLink>
                  <NavLink to="/member/wallet" className={({ isActive }) => isActive ? 'member-nav-link active' : 'member-nav-link'}>
                    我的钱包
                  </NavLink>
                  <NavLink to="/member/center" className={({ isActive }) => isActive ? 'member-nav-link active' : 'member-nav-link'}>
                    会员中心
                  </NavLink>
                </aside>
                <main className="member-main-content">
                  <Routes>
                    <Route path="/reservation" element={<Reservation />} />
                    <Route path="/order-history" element={<OrderHistory />} />
                    <Route path="/wallet" element={<Wallet />} />
                    <Route path="/center" element={<MemberCenter />} />
                  </Routes>
                </main>
              </div>
            </div>
          } />
          
          {/* 原有页面路由 */}
          <Route path="/*" element={
            <div className="original-layout">
              {/* 顶部导航栏 */}
              <nav className="nav-bar">
                <h1 className="app-title">Dot-Store</h1>
              </nav>
              
              <div className="app-container">
                {/* 左侧导航菜单 */}
                <aside className="side-nav">
                  <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} end>
                    今日
                  </NavLink>
                  <NavLink to="/record" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
                    记录
                  </NavLink>
                  <NavLink to="/ledger" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
                    账本
                  </NavLink>
                  <NavLink to="/report" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
                    报表
                  </NavLink>
                  <NavLink to="/setting" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
                    设置
                  </NavLink>
                </aside>
                
                {/* 主内容区域 */}
                <main className="main-content">
                  <Routes>
                    <Route path="/" element={<Today />} />
                    <Route path="/record" element={<Record />} />
                    <Route path="/ledger" element={<Ledger />} />
                    <Route path="/report" element={<Report />} />
                    <Route path="/setting" element={<Setting />} />
                  </Routes>
                </main>
              </div>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
