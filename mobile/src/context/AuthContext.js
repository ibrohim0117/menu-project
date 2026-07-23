import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import {
  loginUser,
  registerAndLogin,
  logoutUser,
  getMe,
  isAuthenticated,
} from '../api/authApi';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  // Ilova ochilganda saqlangan tokenni tekshirgunimizcha true
  const [bootstrapping, setBootstrapping] = useState(true);

  useEffect(() => {
    let cancelled = false;

    const restoreSession = async () => {
      if (await isAuthenticated()) {
        const me = await getMe();
        if (!cancelled && me.success) setUser(me.data);
      }
      if (!cancelled) setBootstrapping(false);
    };

    restoreSession();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (username, password) => {
    const result = await loginUser(username, password);
    if (!result.success) return result;

    const me = await getMe();
    if (!me.success) return me;

    setUser(me.data);
    return { success: true, data: me.data };
  }, []);

  const register = useCallback(async (payload) => {
    const result = await registerAndLogin(payload);
    if (!result.success) return result;

    const me = await getMe();
    if (!me.success) return me;

    setUser(me.data);
    return { success: true, data: me.data };
  }, []);

  const logout = useCallback(async () => {
    await logoutUser();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, bootstrapping, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth faqat AuthProvider ichida ishlatiladi');
  return context;
};
