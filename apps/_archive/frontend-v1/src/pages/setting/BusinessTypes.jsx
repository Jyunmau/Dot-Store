import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const BusinessTypes = () => {
  const [businessTypes, setBusinessTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newBusinessType, setNewBusinessType] = useState({
    name: '',
    description: ''
  });

  const SHOP_ID = 1;
  const CONFIG_KEY = 'business_types';

  // 获取业务类型列表
  const fetchBusinessTypes = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.config.get(SHOP_ID, CONFIG_KEY);
      if (response && response.value) {
        setBusinessTypes(JSON.parse(response.value));
      } else {
        // 初始默认数据
        const defaults = [
          { id: 1, name: '堂食', description: '店内用餐订单' },
          { id: 2, name: '外卖', description: '外卖平台订单' },
          { id: 3, name: '食材采购', description: '原料与进货' },
          { id: 4, name: '房租水电', description: '固定运营支出' }
        ];
        setBusinessTypes(defaults);
      }
    } catch (err) {
      if (err.status === 404) {
        // 配置不存在，使用默认值
        setBusinessTypes([
          { id: 1, name: '堂食', description: '店内用餐订单' },
          { id: 2, name: '外卖', description: '外卖平台订单' }
        ]);
      } else {
        console.error('获取业务类型失败:', err);
        setError('获取业务类型失败，请稍后重试');
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
      console.error('更新业务类型到后端失败:', err);
      setError('保存失败，请检查网络');
    }
  };

  // 添加新业务类型
  const addBusinessType = async (e) => {
    e.preventDefault();
    if (!newBusinessType.name.trim()) return;

    const newList = [...businessTypes, { ...newBusinessType, id: Date.now() }];
    setBusinessTypes(newList);
    await saveToBackend(newList);

    setNewBusinessType({ name: '', description: '' });
  };

  // 删除业务类型
  const deleteBusinessType = async (id) => {
    const newList = businessTypes.filter(type => type.id !== id);
    setBusinessTypes(newList);
    await saveToBackend(newList);
  };

  useEffect(() => {
    fetchBusinessTypes();
  }, []);

  return (
    <div className="business-types-page">
      <div className="page-header">
        <h1>业务类型管理</h1>
      </div>

      {/* 添加业务类型表单 */}
      <div className="card level1 add-business-type-form">
        <h2>添加新业务类型</h2>
        <form onSubmit={addBusinessType}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="name">业务类型名称</label>
              <input
                type="text"
                id="name"
                value={newBusinessType.name}
                onChange={(e) => setNewBusinessType({ ...newBusinessType, name: e.target.value })}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="description">业务类型描述</label>
            <textarea
              id="description"
              value={newBusinessType.description}
              onChange={(e) => setNewBusinessType({ ...newBusinessType, description: e.target.value })}
              rows="3"
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="primary" disabled={loading}>
              {loading ? '保存中...' : '添加业务类型'}
            </button>
          </div>
        </form>
      </div>

      {/* 业务类型列表 */}
      <div className="card level1 business-types-list">
        <h2>业务类型列表</h2>
        {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}

        {loading && businessTypes.length === 0 ? (
          <div className="loading-container">
            <div className="loading"></div>
          </div>
        ) : businessTypes.length > 0 ? (
          <table className="business-types-table">
            <thead>
              <tr>
                <th>名称</th>
                <th>描述</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {businessTypes.map((type) => (
                <tr key={type.id} className="business-type-item">
                  <td>{type.name}</td>
                  <td>{type.description}</td>
                  <td>
                    <button className="text danger" onClick={() => deleteBusinessType(type.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <p>暂无业务类型</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BusinessTypes;