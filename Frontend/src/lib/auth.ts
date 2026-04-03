"use client";

const AUTH_KEY = "automatisor_auth";

export interface AuthSession {
  access_token: string;
  refresh_token: string;
  user_id: string;
  account_id: string | null;
  is_admin: boolean;
  email: string;
}

export function getAuthSession(): AuthSession | null {
  if (typeof window === "undefined") return null;
  const raw = sessionStorage.getItem(AUTH_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as AuthSession;
  } catch {
    return null;
  }
}

export function setAuthSession(session: AuthSession): void {
  sessionStorage.setItem(AUTH_KEY, JSON.stringify(session));
}

export function clearAuthSession(): void {
  sessionStorage.removeItem(AUTH_KEY);
}

export function isUnlocked(): boolean {
  return getAuthSession() !== null;
}

export function isAdmin(): boolean {
  return getAuthSession()?.is_admin ?? false;
}
