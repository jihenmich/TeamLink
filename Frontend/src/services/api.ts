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

// Authentifizierungs-Service
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

// Team-Service
export const teamService = {
  getDashboardData: async () => {
    const response = await api.get('/dashboard');
    return response.data;
  },
  getRecentActivity: async () => {
    const response = await api.get('/api/activity');
    return response.data;
  },
  getTeamMembers: async () => {
    const response = await api.get('/api/employees/');
    return response.data;
  },
};

// Leave-Service
export const leaveService = {
  getAllLeaveRequests: async () => {
    const response = await api.get('/api/leave/');
    return response.data;
  },
  requestLeave: async (employeeId: string, startDate: string, endDate: string) => {
    const response = await api.post(`/api/leave/${employeeId}/leave/`, {
      startDate,
      endDate,
    });
    return response.data;
  },
};

// Payroll-Service
export const payrollService = {
  getAllPayrollData: async () => {
    const response = await api.get('/api/payroll/');
    return response.data;
  },
};

// TimeTracking-Service
export const timeTrackingService = {
  getAllTimeTracking: async () => {
    const response = await api.get('/api/time_tracking/');
    return response.data;
  },
};

export default api;
