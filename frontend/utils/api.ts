const API_URL = 'http://localhost:8000';

export const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const api = {
  async post(endpoint: string, data: any) {
    const res = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
      body: JSON.stringify(data),
    });
    return res;
  },

  async get(endpoint: string) {
    const res = await fetch(`${API_URL}${endpoint}`, {
      headers: { ...getAuthHeader() },
    });
    return res;
  },
  
  async put(endpoint: string, data: any) {
    const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
        body: JSON.stringify(data),
      });
      return res;
  }
};
