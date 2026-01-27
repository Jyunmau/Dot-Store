import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../services/api';

const Record = () => {
  const [recordType, setRecordType] = useState('order'); // order, income, expense
  const [formData, setFormData] = useState({
    amount: '',
    type: '',
    tags: [],
    note: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // 从URL状态中获取记录类型
  useEffect(() => {
    if (location.state?.type) {
      const type = location.state.type;
      setRecordType(type);
      
      // 根据记录类型自动设置标签
      let tags = [];
      if (type === 'expense') {
        tags = ['支出'];
      } else if (type === 'income') {
        tags = ['收入'];
      }
      
      setFormData(prev => ({ ...prev, type, tags }));
    }
  }, [location.state?.type]);

  // 表单字段变化处理
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // 标签选择处理
  const handleTagChange = (e) => {
    const tag = e.target.value;
    setFormData(prev => {
      if (prev.tags.includes(tag)) {
        return { ...prev, tags: prev.tags.filter(t => t !== tag) };
      } else {
        return { ...prev, tags: [...prev.tags, tag] };
      }
    });
  };

  // 记录类型选择处理
  const handleTypeChange = (type) => {
    setRecordType(type);
    
    // 根据记录类型自动设置标签
    let tags = [];
    if (type === 'expense') {
      tags = ['支出'];
    } else if (type === 'income') {
      tags = ['收入'];
    }
    
    setFormData(prev => ({ ...prev, type, tags }));
  };

  // 表单提交处理
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      // 验证表单数据
      if (!formData.amount || isNaN(parseFloat(formData.amount))) {
        throw new Error('请输入有效的金额');
      }
      
      // 模拟 shop_id，实际应该从登录状态或上下文获取
      const shopId = 1;
      
      // 根据记录类型调用不同的API
      const recordData = {
        shop_id: shopId,
        amount: parseFloat(formData.amount),
        type: recordType,
        tags: formData.tags,
        metadata: { note: formData.note },
        status: 'recorded'
      };
      
      // 这里根据记录类型调用不同的API，目前只有订单API，所以统一调用订单API
      await api.order.create(recordData);
      
      setSuccess(true);
      
      // 重置表单
      setFormData({
        amount: '',
        type: recordType,
        tags: [],
        note: ''
      });
      
      // 2秒后跳转到首页
      setTimeout(() => {
        navigate('/');
      }, 2000);
      
    } catch (err) {
      setError(err.message || '创建记录失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 取消按钮处理
  const handleCancel = () => {
    navigate('/');
  };

  return (
    <div className="record-page">
      <div className="page-header">
        <h1>记录</h1>
      </div>
      
      {/* 记录类型选择 */}
      <div className="record-type-selection card level1">
        <button 
          className={`record-type-btn ${recordType === 'order' ? 'active' : ''}`}
          onClick={() => handleTypeChange('order')}
        >
          订单记录
        </button>
        <button 
          className={`record-type-btn ${recordType === 'income' ? 'active' : ''}`}
          onClick={() => handleTypeChange('income')}
        >
          收入记录
        </button>
        <button 
          className={`record-type-btn ${recordType === 'expense' ? 'active' : ''}`}
          onClick={() => handleTypeChange('expense')}
        >
          支出记录
        </button>
      </div>
      
      {/* 记录表单 */}
      <div className="record-form-container">
        {success ? (
          <div className="success-message card level1">
            <h3>记录保存成功！</h3>
            <p>2秒后自动返回首页...</p>
          </div>
        ) : (
          <form className="record-form card level1" onSubmit={handleSubmit}>
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
            
            {/* 金额字段 */}
            <div className="form-group">
              <label htmlFor="amount">金额</label>
              <input
                type="number"
                id="amount"
                name="amount"
                value={formData.amount}
                onChange={handleInputChange}
                placeholder="请输入金额"
                step="0.01"
                required
              />
            </div>
            
            {/* 类型字段 */}
            <div className="form-group">
              <label htmlFor="type">类型</label>
              <select
                id="type"
                name="type"
                value={formData.type}
                onChange={handleInputChange}
                required
              >
                <option value="">请选择类型</option>
                {recordType === 'order' && (
                  <>
                    <option value="堂食">堂食</option>
                    <option value="外卖">外卖</option>
                    <option value="自提">自提</option>
                  </>
                )}
                {recordType === 'income' && (
                  <>
                    <option value="销售收入">销售收入</option>
                    <option value="其他收入">其他收入</option>
                  </>
                )}
                {recordType === 'expense' && (
                  <>
                    <option value="食材采购">食材采购</option>
                    <option value="房租水电">房租水电</option>
                    <option value="人员工资">人员工资</option>
                    <option value="其他支出">其他支出</option>
                  </>
                )}
              </select>
            </div>
            
            {/* 标签字段 */}
            <div className="form-group">
              <label>标签</label>
              <div className="tag-selector">
                <label className="tag-option">
                  <input
                    type="checkbox"
                    value="活动"
                    checked={formData.tags.includes('活动')}
                    onChange={handleTagChange}
                  />
                  活动
                </label>
                <label className="tag-option">
                  <input
                    type="checkbox"
                    value="新品"
                    checked={formData.tags.includes('新品')}
                    onChange={handleTagChange}
                  />
                  新品
                </label>
                <label className="tag-option">
                  <input
                    type="checkbox"
                    value="促销"
                    checked={formData.tags.includes('促销')}
                    onChange={handleTagChange}
                  />
                  促销
                </label>
                <label className="tag-option">
                  <input
                    type="checkbox"
                    value="临时"
                    checked={formData.tags.includes('临时')}
                    onChange={handleTagChange}
                  />
                  临时
                </label>
              </div>
              <div className="selected-tags">
                {formData.tags.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
            </div>
            
            {/* 备注字段 */}
            <div className="form-group">
              <label htmlFor="note">备注</label>
              <textarea
                id="note"
                name="note"
                value={formData.note}
                onChange={handleInputChange}
                placeholder="请输入备注信息"
                rows={4}
              ></textarea>
            </div>
            
            {/* 表单操作按钮 */}
            <div className="form-actions">
              <button type="button" className="secondary" onClick={handleCancel} disabled={loading}>
                取消
              </button>
              <button type="submit" className="primary" disabled={loading}>
                {loading ? '保存中...' : '保存记录'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default Record;
