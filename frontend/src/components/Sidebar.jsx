import { Link } from 'react-router-dom';
import { getRole } from '../utils/auth';

function Sidebar() {
  const role = getRole();

  const links = {
    admin: [
      { to: '/admin', label: 'Dashboard' },
      { to: '/admin/export-users', label: 'Export Users' },
      { to: '/admin/export-reflections', label: 'Export Reflections' },
    ],
    coach: [
      { to: '/coach', label: 'Dashboard' },
      { to: '/sessions/assigned', label: 'Sessions' },
    ],
    user: [
      { to: '/user', label: 'Dashboard' },
      { to: '/reflections', label: 'Reflections' },
    ],
  };

  return (
    <aside className="w-64 bg-gray-100 h-screen shadow p-4">
      <h2 className="text-lg font-semibold mb-4 capitalize">{role} Menu</h2>
      <ul className="space-y-2">
        {links[role]?.map(link => (
          <li key={link.to}>
            <Link
              to={link.to}
              className="block p-2 rounded hover:bg-gray-200 text-sm"
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;
