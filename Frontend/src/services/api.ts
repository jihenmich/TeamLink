import axios from 'axios';
import { useAuthStore } from '../store/auth';

const api = axios.create({
  baseURL: 'http://localhost:8000',  // Backend-URL
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API Service Exports
export const authService = {
  login: async (email: string, password: string) => {
    const response = await api.post('/token', new URLSearchParams({
      username: email,
      password: password,
    }));
    return response.data;
  },
  getProfile: async () => {
    const response = await api.get('/auth/profile');
    return response.data;
  },
};

export const teamService = {
  getDashboardData: async () => {
    const response = await api.get('/dashboard');
    return response.data;
  },
};

export default api;
