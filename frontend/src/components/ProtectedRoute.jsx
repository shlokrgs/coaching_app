import { Navigate, Outlet } from 'react-router-dom';
import { getToken, getRole } from '../utils/auth';

function ProtectedRoute({ allowedRoles }) {
  const token = getToken();
  const role = getRole();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to={`/${role}`} replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
