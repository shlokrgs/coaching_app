import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../Context/AuthContext';

function ProtectedRoute({ allowedRoles }) {
  const { token, role } = useAuth();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to={`/${role}`} replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
