import * as SecureStore from 'expo-secure-store';

const ACCESS_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

export const getAccessToken = () => SecureStore.getItemAsync(ACCESS_KEY);
export const getRefreshToken = () => SecureStore.getItemAsync(REFRESH_KEY);

export const saveTokens = async ({ access, refresh }) => {
  const tasks = [];
  if (access) tasks.push(SecureStore.setItemAsync(ACCESS_KEY, access));
  if (refresh) tasks.push(SecureStore.setItemAsync(REFRESH_KEY, refresh));
  await Promise.all(tasks);
};

export const clearTokens = async () => {
  await Promise.all([
    SecureStore.deleteItemAsync(ACCESS_KEY),
    SecureStore.deleteItemAsync(REFRESH_KEY),
  ]);
};
