// DashboardCoach.jsx
import Layout from '../components/Layout';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../services/api';

function DashboardCoach() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get('/coach/dashboard').then(res => setUsers(res.data));
  }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Coach Dashboard</h1>
      <Link to="/sessions/calendar" className="text-blue-600 underline">📅 View Calendar</Link>
      <div className="mt-4">
        <h2 className="text-xl font-semibold mb-2">My Assigned Users</h2>
        <ul className="space-y-2">
          {users.map(user => (
            <li key={user.id} className="border p-3 rounded bg-white shadow">
              <div>{user.name} ({user.email})</div>
              <Link to={`/coach/users/${user.id}/reflections`} className="text-sm text-blue-600 underline">View Reflections</Link>
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  );
}

export default DashboardCoach;