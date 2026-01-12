// API 基础配置
const API_BASE_URL = 'http://localhost:8000/api';

// 封装 fetch API 调用
async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // 默认选项
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  };
  
  try {
    const response = await fetch(url, defaultOptions);
    
    // 检查响应状态
    if (!response.ok) {
      throw new Error(`API 请求失败: ${response.status} ${response.statusText}`);
    }
    
    // 解析响应数据
    return await response.json();
  } catch (error) {
    console.error('API 请求错误:', error);
    throw error;
  }
}

// API 服务对象
const api = {
  // 订单相关 API
  order: {
    create: (orderData) => fetchAPI('/orders', {
      method: 'POST',
      body: JSON.stringify(orderData),
    }),
    get: (orderId) => fetchAPI(`/orders/${orderId}`),
    update: (orderId, orderData) => fetchAPI(`/orders/${orderId}`, {
      method: 'PUT',
      body: JSON.stringify(orderData),
    }),
    list: (shopId) => fetchAPI(`/orders?shop_id=${shopId}`),
  },
  
  // 账务相关 API
  ledger: {
    // 分类账 API
    account: {
      create: (accountData) => fetchAPI('/ledger/accounts', {
        method: 'POST',
        body: JSON.stringify(accountData),
      }),
      list: (shopId) => fetchAPI(`/ledger/accounts?shop_id=${shopId}`),
    },
    
    // 账务分录 API
    entry: {
      create: (entryData) => fetchAPI('/ledger/entries', {
        method: 'POST',
        body: JSON.stringify(entryData),
      }),
      list: (shopId) => fetchAPI(`/ledger/entries?shop_id=${shopId}`),
    },
  },
  
  // 报表相关 API
  report: {
    summary: (shopId, date) => {
      const params = new URLSearchParams({ shop_id: shopId });
      if (date) params.append('date', date);
      return fetchAPI(`/reports/summary?${params.toString()}`);
    },
    incomeStructure: (shopId, date) => {
      const params = new URLSearchParams({ shop_id: shopId });
      if (date) params.append('date', date);
      return fetchAPI(`/reports/income-structure?${params.toString()}`);
    },
    expenseStructure: (shopId, date) => {
      const params = new URLSearchParams({ shop_id: shopId });
      if (date) params.append('date', date);
      return fetchAPI(`/reports/expense-structure?${params.toString()}`);
    },
  },
  
  // 配置相关 API
  config: {
    create: (configData) => fetchAPI('/config', {
      method: 'POST',
      body: JSON.stringify(configData),
    }),
    list: (shopId) => fetchAPI(`/config?shop_id=${shopId}`),
    get: (shopId, key) => fetchAPI(`/config/${key}?shop_id=${shopId}`),
  },
};

export default api;
