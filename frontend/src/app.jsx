// App.jsx
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardUser from './pages/DashboardUser';
import DashboardCoach from './pages/DashboardCoach';
import DashboardAdmin from './pages/DashboardAdmin';
import ReflectionsPage from './pages/ReflectionsPage';
import ToolkitsPage from './pages/ToolkitsPage';
import CoachUserReflectionsPage from './pages/CoachUserReflectionsPage';
import CoachSessionCalendar from './components/CoachSessionCalendar';
import ProtectedRoute from './components/ProtectedRoute';
import Spinner from './components/Spinner';
import { useAuth } from './Context/AuthContext';

function App() {
  const { token, role, loading } = useAuth();

  if (loading) return <Spinner />;
  if (!token) return <Navigate to="/login" />;

  return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<Navigate to={`/${role}`} />} />

        <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
          <Route path="/admin" element={<DashboardAdmin />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["coach"]} />}>
          <Route path="/coach" element={<DashboardCoach />} />
          <Route path="/coach/users/:userId/reflections" element={<CoachUserReflectionsPage />} />
          <Route path="/sessions/calendar" element={<CoachSessionCalendar />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["user"]} />}>
          <Route path="/user" element={<DashboardUser />} />
          <Route path="/reflections" element={<ReflectionsPage />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["user", "coach", "admin"]} />}>
          <Route path="/toolkits" element={<ToolkitsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
  );
}

export default App;