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
  
  // 获取业务类型列表
  const fetchBusinessTypes = async () => {
    try {
      setLoading(true);
      // 模拟数据，实际应该调用API获取
      setBusinessTypes([
        { id: 1, name: '餐饮订单', description: '堂食和外卖订单' },
        { id: 2, name: '食材采购', description: '食材和原料采购' },
        { id: 3, name: '设备维护', description: '设备维修和维护' },
        { id: 4, name: '人员工资', description: '员工工资和福利' }
      ]);
      setError(null);
    } catch (err) {
      console.error('获取业务类型失败:', err);
      setError('获取业务类型失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };
  
  // 添加新业务类型
  const addBusinessType = async (e) => {
    e.preventDefault();
    try {
      // 模拟添加，实际应该调用API
      const newId = businessTypes.length + 1;
      setBusinessTypes([...businessTypes, { ...newBusinessType, id: newId }]);
      // 重置表单
      setNewBusinessType({
        name: '',
        description: ''
      });
    } catch (err) {
      console.error('添加业务类型失败:', err);
      setError('添加业务类型失败，请稍后重试');
    }
  };
  
  // 删除业务类型
  const deleteBusinessType = async (id) => {
    try {
      // 模拟删除，实际应该调用API
      setBusinessTypes(businessTypes.filter(type => type.id !== id));
    } catch (err) {
      console.error('删除业务类型失败:', err);
      setError('删除业务类型失败，请稍后重试');
    }
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
            <button type="submit" className="primary">添加业务类型</button>
          </div>
        </form>
      </div>
      
      {/* 业务类型列表 */}
      <div className="card level1 business-types-list">
        <h2>业务类型列表</h2>
        {loading ? (
          <div className="loading-container">
            <div className="loading"></div>
          </div>
        ) : error ? (
          <div className="error-message">
            <p>{error}</p>
            <button className="primary" onClick={fetchBusinessTypes}>重试</button>
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
                    <button className="text" onClick={() => console.log('编辑业务类型:', type.id)}>编辑</button>
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