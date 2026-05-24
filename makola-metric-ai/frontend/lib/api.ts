export async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `/api${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

export async function login(email: string, password: string) {
  return apiCall('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export async function register(email: string, password: string, name: string) {
  return apiCall('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password, name }),
  });
}

export async function getCurrentUser() {
  return apiCall('/auth/me', {
    method: 'GET',
  });
}

export async function logout() {
  return apiCall('/auth/logout', {
    method: 'POST',
  });
}

export async function convertCurrency(
  amount: number,
  fromCurrency: string,
  toCurrency: string
) {
  return apiCall('/conversion/convert', {
    method: 'POST',
    body: JSON.stringify({ amount, fromCurrency, toCurrency }),
  });
}

export async function getConversionHistory() {
  return apiCall('/conversion/history', {
    method: 'GET',
  });
}

export async function getRegionalAnalysis(region: string) {
  return apiCall(`/conversion/analysis/regional/${region}`, {
    method: 'GET',
  });
}

export async function getAdminStats() {
  return apiCall('/admin/stats', {
    method: 'GET',
  });
}

export async function getAdminUsers() {
  return apiCall('/admin/users', {
    method: 'GET',
  });
}
