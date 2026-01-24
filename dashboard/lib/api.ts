export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const getToken = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("jobmatch_token");
};

export const setToken = (token: string) => {
  if (typeof window === "undefined") return;
  localStorage.setItem("jobmatch_token", token);
};

export const clearToken = () => {
  if (typeof window === "undefined") return;
  localStorage.removeItem("jobmatch_token");
};

export async function apiFetch(path: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return response.json();
}
