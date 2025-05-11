import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { toast } from 'react-toastify';

function RegisterPage() {
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'user' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validateForm = () => {
    const { name, email, password } = form;
    if (!name || !email || !password) {
      setError('All fields are required');
      return false;
    }
    return true;
  };

  const handleRegister = async () => {
    if (!validateForm()) return;

    setLoading(true);
    setError('');
    try {
      await api.post('/user/register', form);
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        (err.response?.data && typeof err.response.data === 'string'
          ? err.response.data
          : 'Registration failed. Please try again.');
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow w-full max-w-md">
        <h2 className="text-xl font-bold mb-4 text-center">Create Account</h2>

        {error && <p className="text-red-600 text-sm mb-4 text-center">{error}</p>}

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

        <button
          onClick={handleRegister}
          disabled={loading}
          className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded"
        >
          {loading ? 'Registering...' : 'Register'}
        </button>

        <p className="text-sm mt-4 text-center">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 underline">
            Login
          </a>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
