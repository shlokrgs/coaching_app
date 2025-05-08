// ReflectionsPage.jsx
import Layout from '../components/Layout';
import { useEffect, useState } from 'react';
import api from '../services/api';
import EditableReflectionCard from '../components/EditableReflectionCard';

function ReflectionsPage() {
  const [reflections, setReflections] = useState([]);

  const loadReflections = async () => {
    const res = await api.get('/reflections');
    setReflections(res.data);
  };

  useEffect(() => {
    loadReflections();
  }, []);

  return (
    <Layout>
      <h2 className="text-xl font-bold mb-4">📝 My Reflections</h2>
      <div className="space-y-4">
        {reflections.map((r) => (
          <EditableReflectionCard
            key={r.id}
            reflection={r}
            onUpdate={loadReflections}
          />
        ))}
      </div>
    </Layout>
  );
}

export default ReflectionsPage;
