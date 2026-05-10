export const API_BASE = '/api';

export async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Unknown fetch error' }));
    throw new Error(errorData.detail || `API request failed with code ${res.status}`);
  }

  return res.json();
}
