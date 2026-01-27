import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const Tags = () => {
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTag, setNewTag] = useState({
    name: '',
    description: ''
  });
  
  // 获取标签列表
  const fetchTags = async () => {
    try {
      setLoading(true);
      // 模拟数据，实际应该调用API获取
      setTags([
        { id: 1, name: '堂食', description: '堂食订单标签' },
        { id: 2, name: '外卖', description: '外卖订单标签' },
        { id: 3, name: '新品', description: '新品促销标签' },
        { id: 4, name: '活动', description: '活动促销标签' }
      ]);
      setError(null);
    } catch (err) {
      console.error('获取标签失败:', err);
      setError('获取标签失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  // 添加新标签
  const addTag = async (e) => {
    e.preventDefault();
    try {
      // 模拟添加，实际应该调用API
      const newId = tags.length + 1;
      setTags([...tags, { ...newTag, id: newId }]);
      // 重置表单
      setNewTag({
        name: '',
        description: ''
      });
    } catch (err) {
      console.error('添加标签失败:', err);
      setError('添加标签失败，请稍后重试');
    }
  };
  
  // 删除标签
  const deleteTag = async (id) => {
    try {
      // 模拟删除，实际应该调用API
      setTags(tags.filter(tag => tag.id !== id));
    } catch (err) {
      console.error('删除标签失败:', err);
      setError('删除标签失败，请稍后重试');
    }
  };
  
  useEffect(() => {
    fetchTags();
  }, []);
  
  return (
    <div className="tags-page">
      <div className="page-header">
        <h1>标签管理</h1>
      </div>
      
      {/* 添加标签表单 */}
      <div className="card level1 add-tag-form">
        <h2>添加新标签</h2>
        <form onSubmit={addTag}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">标签名称</label>
              <input
                type="text"
                id="name"
                value={newTag.name}
                onChange={(e) => setNewTag({ ...newTag, name: e.target.value })}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="description">标签描述</label>
            <textarea
              id="description"
              value={newTag.description}
              onChange={(e) => setNewTag({ ...newTag, description: e.target.value })}
              rows="3"
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="primary">添加标签</button>
          </div>
        </form>
      </div>
      
      {/* 标签列表 */}
      <div className="card level1 tags-list">
        <h2>标签列表</h2>
        {loading ? (
          <div className="loading-container">
            <div className="loading"></div>
          </div>
        ) : error ? (
          <div className="error-message">
            <p>{error}</p>
            <button className="primary" onClick={fetchTags}>重试</button>
          </div>
        ) : tags.length > 0 ? (
          <div className="tags-grid">
            {tags.map((tag) => (
              <div key={tag.id} className="tag-card card level2">
                <div className="tag-info">
                  <h3 className="tag-name">{tag.name}</h3>
                  <p className="tag-description">{tag.description}</p>
                </div>
                <div className="tag-actions">
                  <button className="text" onClick={() => console.log('编辑标签:', tag.id)}>编辑</button>
                  <button className="text danger" onClick={() => deleteTag(tag.id)}>删除</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>暂无标签</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Tags;