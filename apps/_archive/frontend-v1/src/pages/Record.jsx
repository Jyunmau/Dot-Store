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
  const [options, setOptions] = useState({
    businessTypes: [],
    availableTags: []
  });
  const [loading, setLoading] = useState(false);
  const [fetchingOptions, setFetchingOptions] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const SHOP_ID = 1;

  // 获取动态选项
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        setFetchingOptions(true);
        const [btRes, tagRes] = await Promise.all([
          api.config.get(SHOP_ID, 'business_types'),
          api.config.get(SHOP_ID, 'available_tags')
        ]);

        setOptions({
          businessTypes: btRes?.value ? JSON.parse(btRes.value) : [],
          availableTags: tagRes?.value ? JSON.parse(tagRes.value) : []
        });
      } catch (err) {
        console.error('获取选项失败:', err);
        // 如果 API 失败，使用最基础的备选
        setOptions({
          businessTypes: [
            { id: 'default1', name: '一般订单' },
            { id: 'default2', name: '其它' }
          ],
          availableTags: [
            { id: 'tag1', name: '常规' }
          ]
        });
      } finally {
        setFetchingOptions(false);
      }
    };
    fetchOptions();
  }, []);

  // 从URL状态中获取记录类型
  useEffect(() => {
    if (location.state?.type) {
      const type = location.state.type;
      setRecordType(type);

      let initialTags = [];
      if (type === 'expense') initialTags = ['支出'];
      else if (type === 'income') initialTags = ['收入'];

      setFormData(prev => ({ ...prev, type: '', tags: initialTags }));
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
    let initialTags = [];
    if (type === 'expense') initialTags = ['支出'];
    else if (type === 'income') initialTags = ['收入'];

    setFormData(prev => ({ ...prev, type: '', tags: initialTags }));
  };

  // 表单提交处理
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError(null);

      if (!formData.amount || isNaN(parseFloat(formData.amount)) || parseFloat(formData.amount) <= 0) {
        throw new Error('请输入大于0的有效金额');
      }

      const recordData = {
        shop_id: SHOP_ID,
        amount: parseFloat(formData.amount),
        type: recordType,
        tags: formData.tags,
        metadata: {
          note: formData.note,
          business_type: formData.type // 保存选中的业务类型
        },
        status: 'recorded'
      };

      await api.order.create(recordData);
      setSuccess(true);

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

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <div className="record-page">
      <div className="page-header">
        <h1>记录</h1>
      </div>

      <div className="record-type-selection card level1">
        {['order', 'income', 'expense'].map(type => (
          <button
            key={type}
            className={`record-type-btn ${recordType === type ? 'active' : ''}`}
            onClick={() => handleTypeChange(type)}
          >
            {type === 'order' ? '订单记录' : type === 'income' ? '收入记录' : '支出记录'}
          </button>
        ))}
      </div>

      <div className="record-form-container">
        {success ? (
          <div className="success-message card level1">
            <h3>记录保存成功！</h3>
            <p>2秒后自动返回首页...</p>
          </div>
        ) : (
          <form className="record-form card level1" onSubmit={handleSubmit}>
            {error && <div className="error-message">{error}</div>}

            <div className="form-group">
              <label htmlFor="amount">金额</label>
              <input
                type="number"
                id="amount"
                name="amount"
                value={formData.amount}
                onChange={handleInputChange}
                placeholder="0.00"
                step="0.01"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="type">业务类型</label>
              <select
                id="type"
                name="type"
                value={formData.type}
                onChange={handleInputChange}
                required
                disabled={fetchingOptions}
              >
                <option value="">{fetchingOptions ? '加载中...' : '请选择类型'}</option>
                {options.businessTypes.map(bt => (
                  <option key={bt.id} value={bt.name}>{bt.name}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>标签</label>
              <div className="tag-selector">
                {options.availableTags.map(tag => (
                  <label key={tag.id} className="tag-option">
                    <input
                      type="checkbox"
                      value={tag.name}
                      checked={formData.tags.includes(tag.name)}
                      onChange={handleTagChange}
                    />
                    {tag.name}
                  </label>
                ))}
              </div>
              <div className="selected-tags">
                {formData.tags.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="note">备注</label>
              <textarea
                id="note"
                name="note"
                value={formData.note}
                onChange={handleInputChange}
                placeholder="补充信息..."
                rows={4}
              ></textarea>
            </div>

            <div className="form-actions">
              <button type="button" className="secondary" onClick={handleCancel} disabled={loading}>
                取消
              </button>
              <button type="submit" className="primary" disabled={loading || fetchingOptions}>
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
