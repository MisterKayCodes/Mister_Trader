const API_BASE = '/api/v1'

async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem('token')
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'API request failed')
  }

  return response.json()
}

export const api = {
  getStats: () => fetchAPI('/analytics/stats'),
  getSessions: () => fetchAPI('/analytics/sessions'),
  getStrategies: () => fetchAPI('/strategies'),
  getHourly: () => fetchAPI('/analytics/hourly'),
  
  getTrades: (params = {}) => {
    const query = new URLSearchParams(params).toString()
    return fetchAPI(`/trades${query ? `?${query}` : ''}`)
  },
  
  getStrategiesList: () => fetchAPI('/strategies'),
  createStrategy: (data) => fetchAPI('/strategies', { 
    method: 'POST', 
    body: JSON.stringify(data) 
  }),
  deleteStrategy: (id) => fetchAPI(`/strategies/${id}`, { method: 'DELETE' }),
  
  getPlans: () => fetchAPI('/plans'),
  getTodayPlan: () => fetchAPI('/plans/today'),
  createPlan: (data) => fetchAPI('/plans', { 
    method: 'POST', 
    body: JSON.stringify(data) 
  }),
  deletePlan: (id) => fetchAPI(`/plans/${id}`, { method: 'DELETE' }),
  
  exportTrades: () => {
    window.open(`${API_BASE}/export/trades/csv`, '_blank')
  }
}
