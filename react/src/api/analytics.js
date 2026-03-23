import axios from 'axios';

const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || '/api/v1';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    Authorization: `Bearer ${token}`
  };
};

const analyticsApi = {
  getStats: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/stats`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  getSessions: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/sessions`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  getStrategies: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/strategies`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  getSymbols: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/symbols`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  getDays: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/days`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  getPsychology: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/psychology`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  getHourly: async () => {
    const response = await axios.get(`${API_BASE_URL}/analytics/hourly`, {
      headers: getAuthHeaders()
    });
    return response?.data;
  },

  refreshAnalytics: async () => {
    const response = await axios.post(`${API_BASE_URL}/analytics/refresh`, {}, {
      headers: getAuthHeaders()
    });
    return response?.data;
  }
};

export default analyticsApi;