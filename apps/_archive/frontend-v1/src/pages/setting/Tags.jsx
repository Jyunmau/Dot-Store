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

  const SHOP_ID = 1;
  const CONFIG_KEY = 'available_tags';

  // 获取标签列表
  const fetchTags = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.config.get(SHOP_ID, CONFIG_KEY);
      if (response && response.value) {
        setTags(JSON.parse(response.value));
      } else {
        // 初始默认数据
        const defaults = [
          { id: 1, name: '堂食', description: '店内用餐' },
          { id: 2, name: '外卖', description: '外送平台' },
          { id: 3, name: '活动', description: '营销活动相关' },
          { id: 4, name: '支出', description: '标志性支出' }
        ];
        setTags(defaults);
      }
    } catch (err) {
      if (err.status === 404) {
        setTags([
          { id: 1, name: '堂食', description: '店内用餐' },
          { id: 2, name: '外卖', description: '外送平台' }
        ]);
      } else {
        console.error('获取标签失败:', err);
        setError('获取标签失败，请稍后重试');
      }
    } finally {
      setLoading(false);
    }
  };

  // 保存到后端
  const saveToBackend = async (data) => {
    try {
      await api.config.create({
        shop_id: SHOP_ID,
        key: CONFIG_KEY,
        value: JSON.stringify(data)
      });
    } catch (err) {
      console.error('更新标签到后端失败:', err);
      setError('保存失败，请检查网络');
    }
  };

  // 添加新标签
  const addTag = async (e) => {
    e.preventDefault();
    if (!newTag.name.trim()) return;

    const newList = [...tags, { ...newTag, id: Date.now() }];
    setTags(newList);
    await saveToBackend(newList);

    setNewTag({ name: '', description: '' });
  };

  // 删除标签
  const deleteTag = async (id) => {
    const newList = tags.filter(tag => tag.id !== id);
    setTags(newList);
    await saveToBackend(newList);
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
            <button type="submit" className="primary" disabled={loading}>
              {loading ? '保存中...' : '添加标签'}
            </button>
          </div>
        </form>
      </div>

      {/* 标签列表 */}
      <div className="card level1 tags-list">
        <h2>标签列表</h2>
        {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}

        {loading && tags.length === 0 ? (
          <div className="loading-container">
            <div className="loading"></div>
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