import axios, { AxiosResponse } from 'axios';
import {
  AuthResponse,
  UserProfile,
  UserSettings,
  ChatResponse,
  IntegrationStatus,
  MCPStartResponse
} from './types';

const API_BASE_URL = 'http://localhost:4000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return Promise.reject(new Error('Session expired. Please login again.'));
    }

    // Handle other error statuses
    if (error.response?.status === 403) {
      return Promise.reject(new Error('Access denied. Admin privileges required.'));
    }

    if (error.response?.status === 404) {
      return Promise.reject(new Error('Resource not found.'));
    }

    if (error.response?.status === 500) {
      return Promise.reject(new Error('Server error. Please try again later.'));
    }

    // Handle network errors
    if (!error.response) {
      return Promise.reject(new Error('Network error. Please check your connection.'));
    }

    // Return the error message from server if available
    const message = error.response?.data?.message || error.response?.data?.error || error.message;
    return Promise.reject(new Error(message));
  }
);

export const authApi = {
  login: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/login', { email, password }),

  signup: (name: string, email: string, password: string): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/signup', { name, email, password }),

  me: (): Promise<AxiosResponse<UserProfile>> =>
    api.get('/auth/me'),

  changePassword: (currentPassword: string, newPassword: string): Promise<AxiosResponse<any>> =>
    api.put('/auth/change-password', { currentPassword, newPassword }),
};

export const chatApi = {
  sendMessage: (messages: any[]): Promise<AxiosResponse<ChatResponse>> =>
    api.post('/chat', { messages }),
};

export const settingsApi = {
  getSettings: (): Promise<AxiosResponse<UserSettings>> =>
    api.get('/settings'),

  updateSettings: (settings: Partial<UserSettings & { apiKey?: string }>): Promise<AxiosResponse<any>> =>
    api.put('/settings', settings),
};

export const integrationsApi = {
  getStatus: (): Promise<AxiosResponse<IntegrationStatus>> =>
    api.get('/integrations/status'),

  startMcp: (): Promise<AxiosResponse<MCPStartResponse>> =>
    api.post('/mcp/start'),

  stopMcp: (): Promise<AxiosResponse<any>> =>
    api.post('/mcp/stop'),

  getMcpStatus: (): Promise<AxiosResponse<any>> =>
    api.get('/mcp/status'),
};

export const adminApi = {
  getUsers: (page: number = 1, limit: number = 10, search?: string): Promise<AxiosResponse<any>> =>
    api.get(`/admin/users?page=${page}&limit=${limit}${search ? `&search=${search}` : ''}`),

  getUser: (id: string): Promise<AxiosResponse<any>> =>
    api.get(`/admin/users/${id}`),

  updateUser: (id: string, data: any): Promise<AxiosResponse<any>> =>
    api.patch(`/admin/users/${id}`, data),

  deleteUser: (id: string): Promise<AxiosResponse<any>> =>
    api.delete(`/admin/users/${id}`),

  getStats: (): Promise<AxiosResponse<any>> =>
    api.get('/admin/stats'),

  // Gemini Keys
  getGeminiKeys: (): Promise<AxiosResponse<any>> =>
    api.get('/admin/gemini-keys'),

  addGeminiKey: (data: { name: string; key: string }): Promise<AxiosResponse<any>> =>
    api.post('/admin/gemini-keys', data),

  updateGeminiKey: (id: string, data: any): Promise<AxiosResponse<any>> =>
    api.patch(`/admin/gemini-keys/${id}`, data),

  deleteGeminiKey: (id: string): Promise<AxiosResponse<any>> =>
    api.delete(`/admin/gemini-keys/${id}`),

  // Settings
  getSettings: (): Promise<AxiosResponse<any>> =>
    api.get('/admin/settings'),

  updateSettings: (data: any): Promise<AxiosResponse<any>> =>
    api.patch('/admin/settings', data),

  // Logs
  getLogs: (page: number = 1, limit: number = 50, filters?: any): Promise<AxiosResponse<any>> => {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    });

    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value.toString());
      });
    }

    return api.get(`/admin/logs?${params}`);
  },

  getLogStats: (): Promise<AxiosResponse<any>> =>
    api.get('/admin/logs/stats'),

  clearOldLogs: (days: number = 30): Promise<AxiosResponse<any>> =>
    api.delete(`/admin/logs?days=${days}`),
};