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
    getAll() {
        return api.get('/recipes/');
    },
    get(id) {
        return api.get(`/recipes/${id}/`);
    },
    create(data) {
        return api.post('/recipes/', data);
    },
    update(id, data) {
        return api.put(`/recipes/${id}/`, data);
    },
    delete(id) {
        return api.delete(`/recipes/${id}/`);
    },
    importFromUrl(url) {
        return api.post('/recipes/import/', { url });
    }
};

// Event API endpoints
export const eventApi = {
    getAll() {
        return api.get('/events/');
    },
    get(id) {
        return api.get(`/events/${id}/`);
    },
    create(data) {
        return api.post('/events/', data);
    },
    update(id, data) {
        return api.put(`/events/${id}/`, data);
    },
    delete(id) {
        return api.delete(`/events/${id}/`);
    }
};

// Meal Plan API endpoints
export const mealPlanApi = {
    getAll() {
        return api.get('/meal-plans/');
    },
    get(id) {
        return api.get(`/meal-plans/${id}/`);
    },
    create(data) {
        return api.post('/meal-plans/', data);
    },
    update(id, data) {
        return api.put(`/meal-plans/${id}/`, data);
    },
    delete(id) {
        return api.delete(`/meal-plans/${id}/`);
    },
    createSlots(planId, slots) {
        return api.post(`/meal-plans/${planId}/bulk_create_slots/`, { slots });
    },
    getAllSlots() {
        return api.get('/meal-slots/');
    },
    getSlot(id) {
        return api.get(`/meal-slots/${id}/`);
    },
    updateSlot(id, data) {
        return api.put(`/meal-slots/${id}/`, data);
    },
    deleteSlot(id) {
        return api.delete(`/meal-slots/${id}/`);
    }
};

// Auth API endpoints
export const authApi = {
    login(username, password) {
        return api.post('/token/', { username, password });
    },
    refresh(refresh_token) {
        return api.post('/token/refresh/', { refresh: refresh_token });
    }
};

export default api;
