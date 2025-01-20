import axios from 'axios';

// API Configuration
const config = {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
};

// Create axios instance with default config
const api = axios.create({
    baseURL: config.baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor to add JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If error is 401 and we haven't tried refreshing yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Try to refresh the token
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) {
                    throw new Error('No refresh token available');
                }

                const response = await axios.post(`${config.baseURL}/token/refresh/`, {
                    refresh: refreshToken
                });

                // Store the new access token
                const { access } = response.data;
                localStorage.setItem('access_token', access);

                // Update the failed request with new token and retry
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // If refresh fails, clear tokens and redirect to login
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Recipe API endpoints
export const recipeApi = {
    getAll: () => api.get('/recipes/'),
    get: (id) => api.get(`/recipes/${id}/`),
    create: (data) => api.post('/recipes/', data),
    update: (id, data) => api.put(`/recipes/${id}/`, data),
    delete: (id) => api.delete(`/recipes/${id}/`),
    importFromUrl: (url) => api.post('/recipes/import-from-url/', { url })
};

// Event API endpoints
export const eventApi = {
    getAll: () => api.get('/events/'),
    get: (id) => api.get(`/events/${id}/`),
    create: (data) => api.post('/events/', data),
    update: (id, data) => api.put(`/events/${id}/`, data),
    delete: (id) => api.delete(`/events/${id}/`)
};

// Auth API endpoints
export const authApi = {
    login: (username, password) => 
        axios.post(`${config.baseURL}/token/`, { username, password }),
    refresh: (refresh_token) => 
        axios.post(`${config.baseURL}/token/refresh/`, { refresh: refresh_token }),
};

export default api;
