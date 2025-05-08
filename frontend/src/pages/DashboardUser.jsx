// DashboardUser.jsx
import Layout from '../components/Layout';
import { Link } from 'react-router-dom';

function DashboardUser() {
  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Welcome to Your Dashboard</h1>
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2">
        <Link to="/reflections" className="p-4 bg-blue-50 border rounded shadow hover:bg-blue-100">
          ✍️ Journal Reflections
        </Link>
        <Link to="/toolkits" className="p-4 bg-green-50 border rounded shadow hover:bg-green-100">
          🧰 Explore Toolkits
        </Link>
      </div>
    </Layout>
  );
}

export default DashboardUser;
