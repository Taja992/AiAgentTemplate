import { Api } from './api/api';
import { API_CONFIG } from '../config/apiConfig';

const apiClient = new Api({
    baseURL: API_CONFIG.baseURL,
    timeout: API_CONFIG.timeout,
    withCredentials: API_CONFIG.withCredentials
  });



  apiClient.instance.interceptors.request.use((config) => {
        // Authentication later goes here
        // const token = localStorage.getItem('token');
        // if (token) {
        //   config.headers.Authorization = `Bearer ${token}`;
    
        console.debug('API Request:', config.method?.toUpperCase(), config.url);
        return config;
      });

      apiClient.instance.interceptors.response.use(
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


export { apiClient };