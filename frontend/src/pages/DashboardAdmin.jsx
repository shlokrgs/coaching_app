import Layout from '../components/Layout';
import { useEffect, useState } from 'react';
import api from '../services/api';

function DashboardAdmin() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    api.get('/admin/summary').then(res => setSummary(res.data));
  }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
      {summary && (
        <ul className="space-y-2">
          <li>👥 Users: {summary.total_users}</li>
          <li>📝 Reflections: {summary.total_reflections}</li>
          <li>📆 Sessions: {summary.total_sessions}</li>
          <li>🗒️ Coach Notes: {summary.total_coach_notes}</li>
        </ul>
      )}
    </Layout>
  );
}

export default DashboardAdmin;
