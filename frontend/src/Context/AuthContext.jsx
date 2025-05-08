// src/context/AuthContext.jsx
import { createContext, useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
      api.get('/user/me')
        .then((res) => {
          setUserId(res.data.user_id);
          return api.get(`/user/${res.data.user_id}`);
        })
        .then((res) => {
          setToken(storedToken);
          setRole(res.data.role);
        })
        .catch(() => {
          logout();
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = (token, userRole, userId) => {
    localStorage.setItem('token', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    setToken(token);
    setRole(userRole);
    setUserId(userId);
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    setToken(null);
    setRole(null);
    setUserId(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ token, role, userId, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
