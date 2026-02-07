import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Ledger = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    accountType: 'all',
    startDate: '',
    endDate: ''
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
  const [showEditModal, setShowEditModal] = useState(null);
  const [editFormData, setEditFormData] = useState({
    amount: '',
    note: '',
    type: ''
  });
  const navigate = useNavigate();

  // 获取账务记录
  const fetchRecords = async () => {
    try {
      setLoading(true);

      // 模拟 shop_id，实际应该从登录状态或上下文获取
      const shopId = 1;

      // 获取记录列表
      let recordsData = [];
      try {
        recordsData = await api.order.list(shopId);

        // 处理recordsData，确保amount_estimate字段有值
        const processedRecords = recordsData.map(record => {
          return {
            ...record,
            amount_estimate: (record.amount_estimate || record.amount || 0)
          };
        });

        setRecords(processedRecords);
      } catch (err) {
        console.error('获取记录列表失败:', err);
        setRecords([]);
      }

      setError(null);
    } catch (err) {
      console.error('获取账务记录失败:', err);
      setError('获取账务记录失败，请稍后重试');
      setRecords([]);
    } finally {
      setLoading(false);
    }
  };

  // 筛选记录
  const filteredRecords = records.filter(record => {
    // 账户类型筛选
    if (filters.accountType !== 'all') {
      const isExpense = record.tags?.includes('支出') || (record.metadata?.note && record.metadata.note.includes('支出'));
      if (filters.accountType === 'income' && isExpense) return false;
      if (filters.accountType === 'expense' && !isExpense) return false;
    }

    // 日期范围筛选
    if (filters.startDate && new Date(record.created_at) < new Date(filters.startDate)) return false;
    if (filters.endDate && new Date(record.created_at) > new Date(filters.endDate)) return false;

    // 搜索筛选
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      return (
        record.metadata?.note?.toLowerCase().includes(searchLower) ||
        record.type?.toLowerCase().includes(searchLower) ||
        record.tags?.some(tag => tag.toLowerCase().includes(searchLower))
      );
    }

    return true;
  });

  // 打开编辑模态框
  const editRecord = (record) => {
    setEditFormData({
      amount: record.amount_estimate || 0,
      note: record.metadata?.note || '',
      type: record.type || ''
    });
    setShowEditModal(record.id);
  };

  // 保存编辑
  const saveEdit = async () => {
    if (!showEditModal) return;

    try {
      setLoading(true);

      await api.order.update(showEditModal, {
        amount: parseFloat(editFormData.amount),
        metadata: { note: editFormData.note },
        type: editFormData.type
      });

      // 关闭模态框并刷新列表
      setShowEditModal(null);
      await fetchRecords();
    } catch (err) {
      console.error('更新记录失败:', err);
      setError('更新记录失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 删除记录
  const deleteRecord = async (recordId) => {
    try {
      setLoading(true);

      // 调用删除API
      await api.order.delete(recordId);

      // 更新记录列表
      setRecords(prev => prev.filter(record => record.id !== recordId));
      setShowDeleteConfirm(null);
    } catch (err) {
      console.error('删除记录失败:', err);
      setError('删除记录失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 筛选条件变化处理
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  // 搜索词变化处理
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  return (
    <div className="ledger-page">
      <div className="page-header">
        <h1>分类账</h1>
      </div>

      {/* 筛选和搜索区域 */}
      <div className="filters-search-section card level1">
        <div className="filters-container">
          <div className="filter-group">
            <label htmlFor="accountType">账目类型</label>
            <select
              id="accountType"
              name="accountType"
              value={filters.accountType}
              onChange={handleFilterChange}
            >
              <option value="all">全部</option>
              <option value="income">收入</option>
              <option value="expense">支出</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="startDate">开始日期</label>
            <input
              type="date"
              id="startDate"
              name="startDate"
              value={filters.startDate}
              onChange={handleFilterChange}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="endDate">结束日期</label>
            <input
              type="date"
              id="endDate"
              name="endDate"
              value={filters.endDate}
              onChange={handleFilterChange}
            />
          </div>
        </div>

        <div className="search-container">
          <input
            type="text"
            placeholder="搜索记录"
            value={searchTerm}
            onChange={handleSearchChange}
          />
        </div>
      </div>

      {loading ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="loading"></div>
        </div>
      ) : error ? (
        <div className="card level1" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px' }}>
          <div className="error" style={{ color: '#F5222D', textAlign: 'center' }}>
            <p>{error}</p>
            <button className="primary" onClick={fetchRecords} style={{ marginTop: '16px' }}>重试</button>
          </div>
        </div>
      ) : (
        <div className="records-section">
          <div className="records-list card level1">
            {filteredRecords.length > 0 ? (
              filteredRecords.map((record) => (
                <div key={record.id} className="ledger-record-item">
                  <div className="record-date">
                    {new Date(record.created_at).toLocaleDateString()}
                  </div>
                  <div className="record-desc">
                    <h4>{record.metadata?.note || '无描述'}</h4>
                    <p className="record-type">{record.type}</p>
                  </div>
                  <div className={record.tags?.includes('支出') || (record.metadata?.note && record.metadata.note.includes('支出')) ? 'record-amount expense' : 'record-amount income'}>
                    {(record.tags?.includes('支出') || (record.metadata?.note && record.metadata.note.includes('支出'))) ? '-' : '+'}{'¥'}{(record.amount_estimate || 0).toFixed(2)}
                  </div>
                  <div className="record-actions">
                    <button className="text" onClick={() => editRecord(record)}>编辑</button>
                    <button className="text danger" onClick={() => setShowDeleteConfirm(record.id)}>删除</button>
                  </div>

                  {/* 删除确认框 */}
                  {showDeleteConfirm === record.id && (
                    <div className="delete-confirm">
                      <p>确定要删除这条记录吗？</p>
                      <div className="confirm-actions">
                        <button className="secondary" onClick={() => setShowDeleteConfirm(null)}>取消</button>
                        <button className="danger" onClick={() => deleteRecord(record.id)}>确定</button>
                      </div>
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div className="no-records" style={{ padding: '48px', textAlign: 'center', color: '#8C8C8C' }}>
                <p>暂无符合条件的记录</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 编辑模态框 */}
      {showEditModal && (
        <div className="modal-overlay" onClick={() => setShowEditModal(null)}>
          <div className="modal-content card level3" onClick={e => e.stopPropagation()}>
            <h2>编辑记录</h2>
            <div className="form-group">
              <label htmlFor="edit-amount">金额</label>
              <input
                type="number"
                id="edit-amount"
                value={editFormData.amount}
                onChange={(e) => setEditFormData({ ...editFormData, amount: e.target.value })}
                step="0.01"
              />
            </div>
            <div className="form-group">
              <label htmlFor="edit-note">备注</label>
              <textarea
                id="edit-note"
                value={editFormData.note}
                onChange={(e) => setEditFormData({ ...editFormData, note: e.target.value })}
                rows={3}
              />
            </div>
            <div className="form-actions">
              <button className="secondary" onClick={() => setShowEditModal(null)}>取消</button>
              <button className="primary" onClick={saveEdit}>保存</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Ledger;

