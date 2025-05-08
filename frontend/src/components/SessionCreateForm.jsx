// -- SessionCreateForm.jsx --
import { useEffect, useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

function SessionCreateForm({ onSessionCreated }) {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ user_id: '', requested_at: '', link: '' });

  useEffect(() => {
    api.get('/coach/dashboard').then(res => setUsers(res.data));
  }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    if (!form.user_id || !form.requested_at) {
      toast.error('User and time are required');
      return;
    }
    try {
      await api.post('/sessions', form);
      toast.success('✅ Session scheduled');
      setForm({ user_id: '', requested_at: '', link: '' });
      onSessionCreated?.();
    } catch {
      toast.error('❌ Could not schedule session');
    }
  };

  return (
    <div className="border p-4 rounded bg-white shadow mb-4">
      <h3 className="text-lg font-bold mb-2">📅 Schedule a New Session</h3>
      <select name="user_id" className="w-full p-2 border mb-2 rounded" value={form.user_id} onChange={handleChange}>
        <option value="">-- Select User --</option>
        {users.map(user => (
          <option key={user.id} value={user.id}>{user.name} ({user.email})</option>
        ))}
      </select>
      <input type="datetime-local" name="requested_at" className="w-full p-2 border mb-2 rounded" value={form.requested_at} onChange={handleChange} />
      <input type="url" name="link" className="w-full p-2 border mb-2 rounded" placeholder="Optional Zoom/Calendly link" value={form.link} onChange={handleChange} />
      <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">Schedule Session</button>
    </div>
  );
}

export default SessionCreateForm;
