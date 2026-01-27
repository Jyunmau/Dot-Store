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
          // 使用record.amount作为备选，因为前端传递的是amount字段
          // 但后端返回时使用的是amount_estimate字段
          return {
            ...record,
            // 优先使用record.amount_estimate，如果没有则使用record.amount，如果都没有则使用0
            amount_estimate: (record.amount_estimate || record.amount || 0)
          };
        });
        
        setRecords(processedRecords);
      } catch (err) {
        console.error('获取记录列表失败:', err);
        // 使用模拟数据
        setRecords([
          {
            id: 1,
            created_at: '2024-01-18T12:30:00Z',
            amount_estimate: 123,
            type: '堂食',
            tags: ['堂食'],
            metadata: { note: '餐饮订单' },
            status: 'recorded'
          },
          {
            id: 2,
            created_at: '2024-01-18T10:00:00Z',
            amount_estimate: 50,
            type: '食材采购',
            tags: ['支出'],
            metadata: { note: '食材采购' },
            status: 'recorded'
          },
          {
            id: 3,
            created_at: '2024-01-17T18:45:00Z',
            amount_estimate: 234,
            type: '外卖',
            tags: ['外卖'],
            metadata: { note: '外卖订单' },
            status: 'recorded'
          }
        ]);
      }
      
      setError(null);
    } catch (err) {
      console.error('获取账务记录失败:', err);
      setError('获取账务记录失败，请稍后重试');
      // 使用模拟数据
      setRecords([
        {
          id: 1,
          created_at: '2024-01-18T12:30:00Z',
          amount: 123,
          type: '堂食',
          tags: ['堂食'],
          metadata: { note: '餐饮订单' },
          status: 'recorded'
        },
        {
          id: 2,
          created_at: '2024-01-18T10:00:00Z',
          amount: 50,
          type: '食材采购',
          tags: ['支出'],
          metadata: { note: '食材采购' },
          status: 'recorded'
        },
        {
          id: 3,
          created_at: '2024-01-17T18:45:00Z',
          amount: 234,
          type: '外卖',
          tags: ['外卖'],
          metadata: { note: '外卖订单' },
          status: 'recorded'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 筛选记录
  const filteredRecords = records.filter(record => {
    // 账户类型筛选 - 由于当前只有订单数据，暂时不进行类型筛选
    // 日期范围筛选
    if (filters.startDate && new Date(record.created_at) < new Date(filters.startDate)) return false;
    if (filters.endDate && new Date(record.created_at) > new Date(filters.endDate)) return false;
    
    // 搜索筛选
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      return (
        record.metadata?.note.toLowerCase().includes(searchLower) ||
        record.type?.toLowerCase().includes(searchLower) ||
        record.tags?.some(tag => tag.toLowerCase().includes(searchLower))
      );
    }
    
    return true;
  });

  // 编辑记录
  const editRecord = (recordId) => {
    navigate(`/record/${recordId}/edit`);
  };

  // 删除记录
  const deleteRecord = async (recordId) => {
    try {
      setLoading(true);
      
      // 模拟 shop_id，实际应该从登录状态或上下文获取
      const shopId = 1;
      
      // 删除记录
      await api.order.delete(shopId, recordId);
      
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
                    <button className="text" onClick={() => editRecord(record.id)}>编辑</button>
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
    </div>
  );
};

export default Ledger;
