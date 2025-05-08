import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await api.post('/user/login', new URLSearchParams({
        username: email,
        password: password
      }));

      localStorage.setItem('token', res.data.access_token);
      const payload = JSON.parse(atob(res.data.access_token.split('.')[1]));
      const role = payload.role || 'user';
      navigate(`/${role}`);
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Login</h2>
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <input
          type="email"
          className="w-full p-2 border rounded mb-2"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          type="password"
          className="w-full p-2 border rounded mb-4"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white px-4 py-2 rounded"
        >
          Login
        </button>
        <p className="text-sm mt-4 text-center">
          Don't have an account? <a href="/register" className="text-blue-600 underline">Register</a>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
