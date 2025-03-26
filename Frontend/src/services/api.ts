import axios from 'axios';
import { useAuthStore } from '../store/auth';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Backend-URL
});

// Token automatisch bei jedem Request anhängen
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
  register: async (email: string, password: string) => {
    const response = await api.post('/register', { email, password });
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
  addTeamMember: async (name: string, role: string, hoursWorked: number) => {
    const response = await api.post('/api/employees/', {
      name,
      role,
      hours_worked: hoursWorked,
    });
    return response.data;
  },
  deleteTeamMember: async (id: string) => {
    const response = await api.delete(`/api/employees/${id}`);
    return response.data;
  },
};

// Leave-Service
export const leaveService = {
  getAllLeaveRequests: async () => {
    const response = await api.get('/api/leave/');
    return response.data;
  },
  requestLeave: async (employeeId: string, startDate: string, endDate: string, status: string = "Pending") => {
    const response = await api.post(`/api/leave/${employeeId}/leave/`, {
      employee_id: Number(employeeId),
      start_date: startDate,  
      end_date: endDate,      
      status,
    });
    return response.data;
  },
  deleteLeave: async (leaveId: string) => {
    const response = await api.delete(`/api/leave/${leaveId}`);
    return response.data;
  },
};

// Payroll-Service
export const payrollService = {
  getAllPayrollData: async () => {
    const response = await api.get('/api/payroll/');
    return response.data;
  },
  addPayroll: async (employeeId: string, salary: number, payrollDate: string, deductions: number) => {
    const response = await api.post('/api/payroll/', {
      employee_id: Number(employeeId),
      salary,
      payroll_date: payrollDate,
      deductions,
    });
    return response.data;
  },
  deletePayroll: async (payrollId: string) => {
    const response = await api.delete(`/api/payroll/${payrollId}`);
    return response.data;
  },
};

// TimeTracking-Service
export const timeTrackingService = {
  getAllTimeTracking: async () => {
    const response = await api.get('/api/time_tracking/');
    return response.data;
  },
  addTimeTracking: async (employeeId: string, clockIn: string, clockOut: string, totalHours: number) => {
    const response = await api.post('/api/time_tracking/', {
      employee_id: Number(employeeId),
      clock_in: clockIn,
      clock_out: clockOut,
      total_hours: totalHours,
    });
    return response.data;
  },
  deleteTimeTracking: async (id: string) => {
    const response = await api.delete(`/api/time_tracking/${id}`);
    return response.data;
  },
};

export default api;
