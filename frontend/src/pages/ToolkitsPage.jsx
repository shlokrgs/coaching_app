// ToolkitsPage.jsx
import Layout from '../components/Layout';
import { useEffect, useState } from 'react';
import api from '../services/api';

function ToolkitsPage() {
  const [tools, setTools] = useState([]);

  useEffect(() => {
    api.get('/module/toolkits').then((res) => setTools(res.data));
  }, []);

  return (
    <Layout>
      <h2 className="text-xl font-bold mb-4">🧰 My Toolkits</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {tools.map((tool) => (
          <div key={tool.title} className="border p-4 rounded bg-white shadow">
            <h3 className="font-semibold">{tool.title}</h3>
            <p className="text-sm text-gray-600">{tool.description}</p>
            <a
              href={tool.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 text-sm underline"
            >
              Open
            </a>
          </div>
        ))}
      </div>
    </Layout>
  );
}

export default ToolkitsPage;
