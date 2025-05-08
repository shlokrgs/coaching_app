import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function RegisterPage() {
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'user' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRegister = async () => {
    try {
      await api.post('/user/register', form);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-6 rounded shadow w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Register</h2>
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <input
          type="text"
          name="name"
          className="w-full p-2 border rounded mb-2"
          placeholder="Full Name"
          value={form.name}
          onChange={handleChange}
        />
        <input
          type="email"
          name="email"
          className="w-full p-2 border rounded mb-2"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          className="w-full p-2 border rounded mb-2"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
        />
        <select
          name="role"
          className="w-full p-2 border rounded mb-4"
          value={form.role}
          onChange={handleChange}
        >
          <option value="user">User</option>
          <option value="coach">Coach</option>
        </select>
        <button onClick={handleRegister} className="w-full bg-green-600 text-white px-4 py-2 rounded">
          Register
        </button>
        <p className="text-sm mt-4 text-center">
          Already have an account? <a href="/login" className="text-blue-600 underline">Login</a>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
