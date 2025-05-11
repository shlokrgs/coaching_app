// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001',
});

// Set token if available
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

// Optional: Add interceptors for error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.warn("🔒 Unauthorized or expired session. Logging out...");
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
