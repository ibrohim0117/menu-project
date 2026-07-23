import api from './axiosInstance';
import { saveTokens, clearTokens, getRefreshToken } from './tokenStorage';

// DRF xatolari: login uchun {detail: "..."}, register uchun {username: ["..."]}
const parseError = (error, fallback) => {
  const data = error.response?.data;
  if (!data) {
    return error.code === 'ECONNABORTED'
      ? "So'rov vaqti tugadi, internetni tekshiring"
      : "Serverga ulanib bo'lmadi";
  }
  if (typeof data === 'string') return data;
  if (data.detail) return data.detail;

  const firstKey = Object.keys(data)[0];
  const firstValue = firstKey ? data[firstKey] : null;
  if (Array.isArray(firstValue)) return firstValue[0];
  if (typeof firstValue === 'string') return firstValue;

  return fallback;
};

export const registerUser = async ({
  username,
  password,
  email = '',
  first_name = '',
  last_name = '',
}) => {
  try {
    const { data } = await api.post(
      '/auth/register/',
      { username, password, email, first_name, last_name },
      { skipAuth: true }
    );
    return { success: true, data };
  } catch (error) {
    return { success: false, error: parseError(error, "Ro'yxatdan o'tishda xatolik yuz berdi") };
  }
};

export const loginUser = async (username, password) => {
  try {
    const { data } = await api.post(
      '/auth/login/',
      { username, password },
      { skipAuth: true }
    );
    await saveTokens(data);
    return { success: true, data };
  } catch (error) {
    return { success: false, error: parseError(error, 'Tizimga kirishda xatolik yuz berdi') };
  }
};

// Ro'yxatdan o'tgach darhol kirish uchun
export const registerAndLogin = async (payload) => {
  const registered = await registerUser(payload);
  if (!registered.success) return registered;
  return loginUser(payload.username, payload.password);
};

export const getMe = async () => {
  try {
    const { data } = await api.get('/me/');
    return { success: true, data };
  } catch (error) {
    return { success: false, error: parseError(error, "Foydalanuvchi ma'lumotlarini olib bo'lmadi") };
  }
};

export const logoutUser = async () => {
  await clearTokens();
};

export const isAuthenticated = async () => {
  return Boolean(await getRefreshToken());
};
