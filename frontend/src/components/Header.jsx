// Header.jsx
import { useAuth } from '../Context/AuthContext';

function Header() {
  const { role, logout } = useAuth();

  return (
    <header className="bg-gray-900 text-white p-4 flex justify-between items-center">
      <h1 className="text-lg font-bold">ALIGN Coaching</h1>
      <div className="flex items-center space-x-4">
        <span className="text-sm uppercase">{role}</span>
        <button onClick={logout} className="text-sm underline">Logout</button>
      </div>
    </header>
  );
}

export default Header;
