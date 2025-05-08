// -- CoachNotePanel.jsx --
import { useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

function CoachNotePanel({ reflectionId, existingNote, reloadNotes }) {
  const [note, setNote] = useState(existingNote?.note || '');
  const [editing, setEditing] = useState(!existingNote);

  const saveNote = async () => {
    try {
      const payload = { reflection_id: reflectionId, note };
      if (existingNote?.id) {
        await api.put(`/coach-notes/${existingNote.id}`, payload);
        toast.success('✏️ Note updated');
      } else {
        await api.post('/coach-notes', payload);
        toast.success('📝 Note added');
      }
      setEditing(false);
      reloadNotes();
    } catch (err) {
      toast.error('❌ Failed to save note');
    }
  };

  return (
    <div className="bg-gray-100 p-3 mt-2 rounded border text-sm">
      <div className="flex justify-between items-center mb-1">
        <span className="font-semibold">Coach Note</span>
        <button className="text-blue-600 text-xs underline" onClick={() => setEditing(!editing)}>
          {editing ? 'Cancel' : existingNote ? 'Edit' : 'Add'}
        </button>
      </div>
      {editing ? (
        <>
          <textarea
            value={note}
            onChange={e => setNote(e.target.value)}
            rows={3}
            className="w-full p-2 border rounded"
            placeholder="Write your note..."
          />
          <button
            onClick={saveNote}
            className="mt-2 bg-blue-600 text-white px-3 py-1 rounded text-sm"
          >
            Save
          </button>
        </>
      ) : (
        <p>{note}</p>
      )}
      {existingNote?.updated_at && (
        <p className="text-gray-500 mt-1 text-xs">
          Last updated: {new Date(existingNote.updated_at).toLocaleString()}
        </p>
      )}
    </div>
  );
}

export default CoachNotePanel;
