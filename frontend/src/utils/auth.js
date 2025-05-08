export function getToken() {
  return localStorage.getItem('token');
}

export function getRole() {
  const payload = JSON.parse(atob(getToken()?.split('.')[1] || '{}'));
  return payload.role || 'user';
}
