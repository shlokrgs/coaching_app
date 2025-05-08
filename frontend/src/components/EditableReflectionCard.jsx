// -- EditableReflectionCard.jsx --
import { useEffect, useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';
import debounce from 'lodash.debounce';

function EditableReflectionCard({ reflection, onUpdate }) {
  const [content, setContent] = useState(reflection.content);
  const [feedback, setFeedback] = useState(reflection.ai_feedback || '');
  const [saving, setSaving] = useState(false);

  const updateReflection = async (newContent) => {
    try {
      setSaving(true);
      const res = await api.put(`/reflections/${reflection.id}`, { content: newContent });
      setFeedback(res.data.ai_feedback);
      toast.success('✅ Feedback updated');
      onUpdate();
    } catch {
      toast.error('❌ Failed to update reflection');
    } finally {
      setSaving(false);
    }
  };

  const debouncedUpdate = debounce((val) => {
    if (val.trim().length > 0 && val !== reflection.content) {
      updateReflection(val);
    }
  }, 1000);

  useEffect(() => {
    debouncedUpdate(content);
    return () => debouncedUpdate.cancel();
  }, [content]);

  return (
    <div className="p-4 border rounded shadow bg-white">
      <textarea
        rows={4}
        value={content}
        onChange={e => setContent(e.target.value)}
        className="w-full p-2 border rounded"
        placeholder="Edit your reflection..."
      />
      <div className="text-sm text-blue-600 mt-2">
        💡 AI Feedback: {saving ? 'Updating...' : feedback}
      </div>
    </div>
  );
}

export default EditableReflectionCard;
