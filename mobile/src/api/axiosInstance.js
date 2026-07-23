import axios from 'axios';
import { getAccessToken, getRefreshToken, saveTokens, clearTokens } from './tokenStorage';

// Terminalda chiqqan local IP manzilingiz
const API_BASE_URL = 'http://192.168.88.199:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  async (config) => {
    if (!config.skipAuth) {
      const token = await getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 401 bo'lganda refresh token bilan bir marta qayta urinamiz.
// Bir vaqtda bir nechta so'rov 401 olsa, bitta refresh so'rovini kutishadi.
let refreshPromise = null;

const refreshAccessToken = async () => {
  const refresh = await getRefreshToken();
  if (!refresh) return null;

  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/auth/refresh/`,
      { refresh },
      { headers: { 'Content-Type': 'application/json' } }
    );
    await saveTokens({ access: data.access, refresh: data.refresh });
    return data.access;
  } catch {
    await clearTokens();
    return null;
  }
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status !== 401 || !original || original._retry || original.skipAuth) {
      return Promise.reject(error);
    }
    original._retry = true;

    if (!refreshPromise) {
      refreshPromise = refreshAccessToken().finally(() => {
        refreshPromise = null;
      });
    }

    const newAccess = await refreshPromise;
    if (!newAccess) return Promise.reject(error);

    original.headers.Authorization = `Bearer ${newAccess}`;
    return api(original);
  }
);

export default api;
