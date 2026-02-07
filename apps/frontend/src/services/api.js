// API 基础配置
const API_BASE_URL = 'http://127.0.0.1:8000/api';

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
    delete: (orderId) => fetchAPI(`/orders/${orderId}`, {
      method: 'DELETE',
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
    summary: (shopId, dateParams) => {
      const params = new URLSearchParams({ shop_id: shopId });
      if (dateParams) {
        if (dateParams.date) params.append('date', dateParams.date);
        if (dateParams.date_range) params.append('date_range', dateParams.date_range);
        if (dateParams.start_date) params.append('start_date', dateParams.start_date);
        if (dateParams.end_date) params.append('end_date', dateParams.end_date);
      }
      return fetchAPI(`/reports/summary?${params.toString()}`);
    },
    incomeStructure: (shopId, dateParams) => {
      const params = new URLSearchParams({ shop_id: shopId });
      if (dateParams) {
        if (dateParams.date) params.append('date', dateParams.date);
        if (dateParams.date_range) params.append('date_range', dateParams.date_range);
        if (dateParams.start_date) params.append('start_date', dateParams.start_date);
        if (dateParams.end_date) params.append('end_date', dateParams.end_date);
      }
      return fetchAPI(`/reports/income-structure?${params.toString()}`);
    },
    expenseStructure: (shopId, dateParams) => {
      const params = new URLSearchParams({ shop_id: shopId });
      if (dateParams) {
        if (dateParams.date) params.append('date', dateParams.date);
        if (dateParams.date_range) params.append('date_range', dateParams.date_range);
        if (dateParams.start_date) params.append('start_date', dateParams.start_date);
        if (dateParams.end_date) params.append('end_date', dateParams.end_date);
      }
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

  // 新增：资源事件相关 API
  resourceEvent: {
    create: (eventData) => fetchAPI('/resource-events', {
      method: 'POST',
      body: JSON.stringify(eventData),
    }),
    get: (eventId) => fetchAPI(`/resource-events/${eventId}`),
    list: (shopId, params = {}) => {
      const urlParams = new URLSearchParams({ shop_id: shopId });
      if (params.resource_id) urlParams.append('resource_id', params.resource_id);
      if (params.resource_type) urlParams.append('resource_type', params.resource_type);
      if (params.event_type) urlParams.append('event_type', params.event_type);
      if (params.start_time) urlParams.append('start_time', params.start_time);
      if (params.end_time) urlParams.append('end_time', params.end_time);
      return fetchAPI(`/resource-events?${urlParams.toString()}`);
    },
  },
};

export default api;
