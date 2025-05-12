// ✅ CoachSessionCalendar.jsx
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { useEffect, useState } from 'react';
import { parseISO } from 'date-fns';
import moment from 'moment';
import api from '../services/api';
import Layout from './Layout';
import { toast } from 'react-toastify';
import SessionCreateForm from './SessionCreateForm';

const localizer = momentLocalizer(moment);

function CoachSessionCalendar() {
  const [events, setEvents] = useState([]);
  const [filterUser, setFilterUser] = useState('');
  const [filterDate, setFilterDate] = useState('');

  const loadSessions = async () => {
    try {
      const res = await api.get('/sessions/assigned');
      const sessions = Array.isArray(res.data)
        ? res.data.map(session => ({
            id: session.id,
            title: `🧑 ${session.user_id} (${session.status})${session.link ? ' 📌' : ''}`,
            start: parseISO(session.requested_at),
            end: parseISO(session.requested_at),
            status: session.status,
          }))
        : [];
      setEvents(sessions);
    } catch (err) {
      console.error('Error loading sessions:', err);
      setEvents([]);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  const handleSelectEvent = (event) => {
    const action = window.prompt(`Session with ${event.title}\nStatus: ${event.status}\nType 'approve', 'reject', or paste Zoom/Calendly link:`);
    if (!action) return;

    const payload = {
      status: ['approve', 'reject'].includes(action) ? action : 'approved',
      link: ['approve', 'reject'].includes(action) ? null : action,
    };

    api.patch(`/sessions/${event.id}`, payload)
      .then(() => {
        toast.success('✅ Session updated');
        loadSessions();
      })
      .catch(() => toast.error('❌ Update failed'));
  };

  const filteredEvents = events.filter(e =>
    (!filterUser || e.title.includes(filterUser)) &&
    (!filterDate || new Date(e.start).toISOString().startsWith(filterDate))
  );

  return (
    <Layout>
      <h2 className="text-xl font-bold mb-4">📅 My Coaching Sessions</h2>

      <SessionCreateForm onSessionCreated={loadSessions} />

      <div className="mb-4">
        <input
          placeholder="Filter by User ID"
          value={filterUser}
          onChange={e => setFilterUser(e.target.value)}
          className="border p-1 rounded mr-2"
        />
        <input
          type="date"
          value={filterDate}
          onChange={e => setFilterDate(e.target.value)}
          className="border p-1 rounded"
        />
      </div>

      <div className="bg-white p-4 rounded shadow">
        <Calendar
          localizer={localizer}
          events={filteredEvents}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 600 }}
          defaultView="week"
          views={['month', 'week', 'day']}
          onSelectEvent={handleSelectEvent}
          eventPropGetter={(event) => ({
            style: {
              backgroundColor:
                event.status === 'approved' ? '#4ade80'
                  : event.status === 'rejected' ? '#f87171'
                  : '#facc15',
              color: '#000',
            },
          })}
        />
      </div>
    </Layout>
  );
}

export default CoachSessionCalendar;