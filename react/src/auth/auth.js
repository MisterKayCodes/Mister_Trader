const TOKEN_KEY = "access_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * Login function
 * Calls your FastAPI login endpoint with telegram_user_id and pin
 * Returns a Promise that resolves on success, rejects on failure
 */
export async function login({ telegram_user_id, pin }) {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api/v1";

  const response = await fetch(`${baseUrl}/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ telegram_user_id, pin })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Login failed");
  }

  const data = await response.json();
  setToken(data.access_token);
  return data;
}

export function logout() {
  clearToken();
}
