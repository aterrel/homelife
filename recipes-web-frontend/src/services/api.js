import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getRecipes = async () => {
  const response = await api.get('/api/recipes/');
  return response.data;
};

export const getRecipe = async (id) => {
  const response = await api.get(`/api/recipes/${id}/`);
  return response.data;
};

export const createRecipe = async (recipeData) => {
  const response = await api.post('/api/recipes/', recipeData);
  return response.data;
};

export const updateRecipe = async (id, recipeData) => {
  const response = await api.put(`/api/recipes/${id}/`, recipeData);
  return response.data;
};

export const deleteRecipe = async (id) => {
  await api.delete(`/api/recipes/${id}/`);
};

export const getCategories = async () => {
  const response = await api.get('/api/categories/');
  return response.data;
};

export const getTags = async () => {
  const response = await api.get('/api/tags/');
  return response.data;
};

export const getIngredients = async () => {
  const response = await api.get('/api/ingredients/');
  return response.data;
};

export default api;
