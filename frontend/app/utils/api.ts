// Create a new file for API utilities

export const setToken = (token: string) => {
  localStorage.setItem('for-the-team-token', token);
};

export const getToken = () => {
  return localStorage.getItem('for-the-team-token');
};

export const clearToken = () => {
  localStorage.removeItem('for-the-team-token');
};

export const fetchWithToken = async (url: string, options: RequestInit = {}) => {
  const token = getToken();
  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  const response = await fetch(url, { ...options, headers });
  if (response.status === 401) {
    // Token might be expired, clear it and redirect to login
    clearToken();
    window.location.href = '/';
  }
  return response;
};