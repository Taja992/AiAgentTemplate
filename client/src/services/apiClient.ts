import { Api } from './api/api';
import { API_CONFIG } from '../config/apiConfig';
import axios from 'axios';

// Create a base axios instance with your config
const axiosInstance = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  withCredentials: API_CONFIG.withCredentials
});

// Add interceptors to the axios instance
axiosInstance.interceptors.request.use((config) => {
  // Authentication later goes here
  // const token = localStorage.getItem('token');
  // if (token) {
  //   config.headers.Authorization = `Bearer ${token}`;
  // }

  console.debug('API Request:', config.method?.toUpperCase(), config.url);
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => {
    console.debug('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:',
      error.response?.status,
      error.response?.config.url,
      error.response?.data || error.message
    );
    return Promise.reject(error);
  }
);

const apiClient = new Api({
  baseUrl: API_CONFIG.baseURL,
  customFetch: async (input, init) => {
    const url =
      typeof input === 'string'
        ? input
        : input instanceof Request
        ? input.url
        : input instanceof URL
        ? input.toString()
        : '';
    
    const response = await axiosInstance({
      url,
      method: init?.method || 'GET',
      data: init?.body,
      headers: init?.headers as any,
      responseType: 'json'
    });
    
    return new Response(new Blob([JSON.stringify(response.data)]), {
      status: response.status,
      statusText: response.statusText,
      headers: new Headers(response.headers as any)
    });
  }
});

export { apiClient };