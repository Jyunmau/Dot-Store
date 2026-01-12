import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import './App.css';

// 导入页面组件
import Today from './pages/Today';
import Record from './pages/Record';
import Ledger from './pages/Ledger';
import Report from './pages/Report';
import Setting from './pages/Setting';

function App() {
  return (
    <Router>
      <div className="App">
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
    </Router>
  );
}

export default App;
