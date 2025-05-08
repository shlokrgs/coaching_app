// CoachUserReflectionsPage.jsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import Layout from '../components/Layout';
import CoachNotePanel from '../components/CoachNotePanel';

function CoachUserReflectionsPage() {
  const { userId } = useParams();
  const [reflections, setReflections] = useState([]);
  const [coachNotes, setCoachNotes] = useState([]);
  const [userInfo, setUserInfo] = useState(null);

  const loadReflections = async () => {
    const [ref, notes, user] = await Promise.all([
      api.get(`/coach/user-reflections/${userId}`),
      api.get(`/coach-notes/user/${userId}`),
      api.get(`/user/${userId}`)
    ]);
    setReflections(ref.data);
    setCoachNotes(notes.data);
    setUserInfo(user.data);
  };

  useEffect(() => {
    loadReflections();
  }, []);

  const groupedReflections = reflections.reduce((acc, r) => {
    const key = `Module ${r.module_id}`;
    acc[key] = acc[key] ? [...acc[key], r] : [r];
    return acc;
  }, {});

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-2">
        Reflections for {userInfo?.name || 'User'}
      </h1>
      {Object.keys(groupedReflections).map((moduleKey) => (
        <div key={moduleKey} className="mb-6">
          <h2 className="text-xl font-semibold mb-2">{moduleKey}</h2>
          <ul className="space-y-4">
            {groupedReflections[moduleKey].map((r) => {
              const note = coachNotes.find(n => n.reflection_id === r.id);
              return (
                <li key={r.id} className="border rounded p-4 shadow bg-white">
                  <div className="text-gray-600 text-sm">
                    Submitted: {new Date(r.submitted_at).toLocaleString()}
                  </div>
                  <p className="mt-2">{r.content}</p>
                  {r.ai_feedback && (
                    <div className="mt-2 text-blue-600 text-sm italic">
                      💡 AI Feedback: {r.ai_feedback}
                    </div>
                  )}
                  <CoachNotePanel
                    reflectionId={r.id}
                    existingNote={note}
                    reloadNotes={loadReflections}
                  />
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </Layout>
  );
}

export default CoachUserReflectionsPage;