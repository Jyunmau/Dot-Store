import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const AccountCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newCategory, setNewCategory] = useState({
    name: '',
    type: 'income', // income or expense
    code: ''
  });

  // 获取账目分类列表
  const fetchCategories = async () => {
    try {
      setLoading(true);
      const shopId = 1; // 实际应该从登录状态获取

      // 调用真实API获取账户列表
      const accounts = await api.ledger.account.list(shopId);

      // 转换数据格式
      const formattedCategories = accounts.map(account => ({
        id: account.id,
        name: account.name,
        type: account.type === '收入账' || account.type === 'income' ? 'income' : 'expense',
        code: account.code
      }));

      setCategories(formattedCategories);
      setError(null);
    } catch (err) {
      console.error('获取账目分类失败:', err);
      setError('获取账目分类失败，请稍后重试');
      // 如果API失败，使用默认数据
      setCategories([
        { id: 1, name: '默认收入账户', type: 'income', code: 'DEFAULT_INCOME' },
        { id: 2, name: '默认成本账户', type: 'expense', code: 'DEFAULT_EXPENSE' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 添加新分类
  const addCategory = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const shopId = 1;

      // 准备API请求数据
      const accountData = {
        shop_id: shopId,
        name: newCategory.name,
        type: newCategory.type === 'income' ? '收入账' : '成本账',
        code: newCategory.code || `CUSTOM_${Date.now()}`
      };

      // 调用API创建账户
      await api.ledger.account.create(accountData);

      // 刷新列表
      await fetchCategories();

      // 重置表单
      setNewCategory({
        name: '',
        type: 'income',
        code: ''
      });

      setError(null);
    } catch (err) {
      console.error('添加账目分类失败:', err);
      setError('添加账目分类失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 删除分类 - 目前API不支持删除，仅做本地移除
  const deleteCategory = async (id) => {
    try {
      // TODO: 需要后端支持删除API
      // 暂时只做本地移除
      setCategories(categories.filter(category => category.id !== id));
    } catch (err) {
      console.error('删除账目分类失败:', err);
      setError('删除账目分类失败，请稍后重试');
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <div className="account-categories-page">
      <div className="page-header">
        <h1>账目分类管理</h1>
      </div>

      {/* 添加分类表单 */}
      <div className="card level1 add-category-form">
        <h2>添加新分类</h2>
        <form onSubmit={addCategory}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">分类名称</label>
              <input
                type="text"
                id="name"
                value={newCategory.name}
                onChange={(e) => setNewCategory({ ...newCategory, name: e.target.value })}
                placeholder="如：餐饮收入、房租支出"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="type">分类类型</label>
              <select
                id="type"
                value={newCategory.type}
                onChange={(e) => setNewCategory({ ...newCategory, type: e.target.value })}
              >
                <option value="income">收入</option>
                <option value="expense">支出</option>
              </select>
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="code">分类代码（选填）</label>
            <input
              type="text"
              id="code"
              value={newCategory.code}
              onChange={(e) => setNewCategory({ ...newCategory, code: e.target.value })}
              placeholder="如：FOOD_INCOME、RENT_EXPENSE"
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="primary" disabled={loading}>
              {loading ? '添加中...' : '添加分类'}
            </button>
          </div>
        </form>
      </div>

      {/* 分类列表 */}
      <div className="card level1 categories-list">
        <h2>账目分类列表</h2>
        {loading ? (
          <div className="loading-container" style={{ display: 'flex', justifyContent: 'center', padding: '32px' }}>
            <div className="loading"></div>
          </div>
        ) : error ? (
          <div className="error-message">
            <p>{error}</p>
            <button className="primary" onClick={fetchCategories}>重试</button>
          </div>
        ) : categories.length > 0 ? (
          <table className="categories-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e2e8f0' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', color: '#64748b' }}>名称</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', color: '#64748b' }}>类型</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', color: '#64748b' }}>代码</th>
                <th style={{ padding: '12px 16px', textAlign: 'right', color: '#64748b' }}>操作</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((category) => (
                <tr key={category.id} className="category-item" style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '16px' }}>{category.name}</td>
                  <td style={{ padding: '16px' }}>
                    <span className={`tag ${category.type === 'income' ? 'income-tag' : 'expense-tag'}`} style={{
                      backgroundColor: category.type === 'income' ? '#d1fae5' : '#fee2e2',
                      color: category.type === 'income' ? '#059669' : '#ef4444',
                      padding: '4px 12px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: '600'
                    }}>
                      {category.type === 'income' ? '收入' : '支出'}
                    </span>
                  </td>
                  <td style={{ padding: '16px', color: '#64748b', fontFamily: 'monospace' }}>{category.code}</td>
                  <td style={{ padding: '16px', textAlign: 'right' }}>
                    <button className="text danger" onClick={() => deleteCategory(category.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state" style={{ padding: '48px', textAlign: 'center', color: '#64748b' }}>
            <p>暂无账目分类，请添加新分类</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AccountCategories;