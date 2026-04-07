"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { API_BASE } from "@/lib/config";

interface User {
  email: string;
  name: string | null;
  token: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("travelmind_user");
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {}
    }
    setLoading(false);
  }, []);

  function saveUser(u: User) {
    setUser(u);
    localStorage.setItem("travelmind_user", JSON.stringify(u));
  }

  async function login(email: string, password: string) {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Đăng nhập thất bại");
    }
    const data = await res.json();
    saveUser({ email: data.email, name: data.name, token: data.token });
  }

  async function register(email: string, password: string, name?: string) {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, name }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Đăng ký thất bại");
    }
    const data = await res.json();
    saveUser({ email: data.email, name: data.name, token: data.token });
  }

  function logout() {
    setUser(null);
    localStorage.removeItem("travelmind_user");
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
