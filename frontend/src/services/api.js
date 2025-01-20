import axios from 'axios';

// API Configuration
const config = {
    baseURL: 'http://localhost:8000/api',  // Hardcode for debugging
    testToken: 'test-token-1234',
};

// Create axios instance with default config
const api = axios.create({
    baseURL: config.baseURL,
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.testToken}`,
    },
});

// Add request interceptor to ensure auth token is always present
api.interceptors.request.use(
    (config) => {
        console.log('Making request to:', config.url);
        console.log('Request headers:', config.headers);
        return config;
    },
    (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

// Add response interceptor to handle errors
api.interceptors.response.use(
    (response) => {
        console.log('Response from:', response.config.url);
        console.log('Response data:', response.data);
        return response;
    },
    (error) => {
        console.error('API Error:', {
            url: error.config?.url,
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            headers: error.config?.headers,
        });
        return Promise.reject(error);
    }
);

// Recipe API endpoints
export const recipeApi = {
    getAll: () => {
        console.log('Fetching all recipes...');
        return api.get('/recipes/');
    },
    get: (id) => api.get(`/recipes/${id}/`),
    create: (data) => {
        console.log('Creating recipe:', data);
        return api.post('/recipes/', data);
    },
    update: (id, data) => {
        console.log('Updating recipe:', id, data);
        return api.put(`/recipes/${id}/`, data);
    },
    delete: (id) => {
        console.log('Deleting recipe:', id);
        return api.delete(`/recipes/${id}/`);
    },
    importFromUrl: (url) => api.post('/recipes/import_from_url/', { url }),
};

export default api;
