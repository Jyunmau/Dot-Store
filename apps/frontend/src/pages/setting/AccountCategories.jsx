import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const AccountCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newCategory, setNewCategory] = useState({
    name: '',
    type: 'income', // income or expense
    description: ''
  });
  
  // 获取账目分类列表
  const fetchCategories = async () => {
    try {
      setLoading(true);
      // 模拟数据，实际应该调用API获取
      setCategories([
        { id: 1, name: '餐饮订单', type: 'income', description: '堂食和外卖订单收入' },
        { id: 2, name: '外卖订单', type: 'income', description: '外卖平台订单收入' },
        { id: 3, name: '食材采购', type: 'expense', description: '食材和原料采购' },
        { id: 4, name: '房租水电', type: 'expense', description: '店铺租金和水电费用' }
      ]);
      setError(null);
    } catch (err) {
      console.error('获取账目分类失败:', err);
      setError('获取账目分类失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  // 添加新分类
  const addCategory = async (e) => {
    e.preventDefault();
    try {
      // 模拟添加，实际应该调用API
      const newId = categories.length + 1;
      setCategories([...categories, { ...newCategory, id: newId }]);
      // 重置表单
      setNewCategory({
        name: '',
        type: 'income',
        description: ''
      });
    } catch (err) {
      console.error('添加账目分类失败:', err);
      setError('添加账目分类失败，请稍后重试');
    }
  };
  
  // 删除分类
  const deleteCategory = async (id) => {
    try {
      // 模拟删除，实际应该调用API
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
            <label htmlFor="description">分类描述</label>
            <textarea
              id="description"
              value={newCategory.description}
              onChange={(e) => setNewCategory({ ...newCategory, description: e.target.value })}
              rows="3"
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="primary">添加分类</button>
          </div>
        </form>
      </div>
      
      {/* 分类列表 */}
      <div className="card level1 categories-list">
        <h2>账目分类列表</h2>
        {loading ? (
          <div className="loading-container">
            <div className="loading"></div>
          </div>
        ) : error ? (
          <div className="error-message">
            <p>{error}</p>
            <button className="primary" onClick={fetchCategories}>重试</button>
          </div>
        ) : categories.length > 0 ? (
          <table className="categories-table">
            <thead>
              <tr>
                <th>名称</th>
                <th>类型</th>
                <th>描述</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((category) => (
                <tr key={category.id} className="category-item">
                  <td>{category.name}</td>
                  <td>{category.type === 'income' ? '收入' : '支出'}</td>
                  <td>{category.description}</td>
                  <td>
                    <button className="text" onClick={() => console.log('编辑分类:', category.id)}>编辑</button>
                    <button className="text danger" onClick={() => deleteCategory(category.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <p>暂无账目分类</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AccountCategories;