import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";
import * as api from "../api/client";

/* ------------------------------------------------------------------ */
/*  Context types                                                      */
/* ------------------------------------------------------------------ */

interface AuthContextValue {
  isAuthenticated: boolean;
  username: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

/* ------------------------------------------------------------------ */
/*  Provider                                                           */
/* ------------------------------------------------------------------ */

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => api.getToken() !== null
  );
  const [username, setUsername] = useState<string | null>(null);

  const login = useCallback(async (user: string, password: string) => {
    const token = await api.login(user, password);
    api.setToken(token.accessToken);
    setUsername(user);
    setIsAuthenticated(true);
  }, []);

  const logout = useCallback(() => {
    api.clearToken();
    setUsername(null);
    setIsAuthenticated(false);
  }, []);

  const value = useMemo(
    () => ({ isAuthenticated, username, login, logout }),
    [isAuthenticated, username, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

/* ------------------------------------------------------------------ */
/*  Login form component                                               */
/* ------------------------------------------------------------------ */

const loginStyles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    background: "linear-gradient(135deg, #f5f6fa 0%, #e8e6f0 40%, #ddd6f3 70%, #d4cce7 100%)",
  },
  card: {
    background: "#fff",
    borderRadius: 16,
    padding: "40px 36px",
    boxShadow: "0 8px 32px rgba(0,0,0,0.10), 0 2px 8px rgba(79,70,229,0.06)",
    width: 380,
    maxWidth: "90vw",
  },
  title: {
    margin: "0 0 4px",
    fontSize: 24,
    fontWeight: 700,
    color: "#1a1a2e",
  },
  tagline: {
    margin: "0 0 6px",
    fontSize: 13,
    color: "#7c3aed",
    fontWeight: 500,
    letterSpacing: 0.2,
  },
  subtitle: {
    margin: "0 0 24px",
    fontSize: 14,
    color: "#888",
  },
  label: {
    display: "block",
    marginBottom: 4,
    fontSize: 13,
    fontWeight: 500,
    color: "#444",
  },
  input: {
    width: "100%",
    padding: "10px 12px",
    marginBottom: 16,
    border: "1px solid #ddd",
    borderRadius: 10,
    fontSize: 15,
    boxSizing: "border-box" as const,
    outline: "none",
    transition: "border-color 0.15s, box-shadow 0.15s",
  },
  button: {
    width: "100%",
    padding: "12px 0",
    background: "linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)",
    color: "#fff",
    border: "none",
    borderRadius: 10,
    fontSize: 15,
    fontWeight: 600,
    cursor: "pointer",
    boxShadow: "0 2px 8px rgba(79,70,229,0.25)",
    transition: "opacity 0.15s, box-shadow 0.15s",
  },
  error: {
    color: "#e53e3e",
    fontSize: 13,
    marginBottom: 12,
  },
};

export function LoginForm() {
  const { login } = useAuth();
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(user, pass);
    } catch {
      setError("Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={loginStyles.wrapper}>
      <form style={loginStyles.card} onSubmit={handleSubmit}>
        <h1 style={loginStyles.title}>🎬 AI Insights Assistant</h1>
        <p style={loginStyles.tagline}>
          Your entertainment data, powered by AI
        </p>
        <p style={loginStyles.subtitle}>Sign in to continue</p>

        {error && <p style={loginStyles.error}>{error}</p>}

        <label style={loginStyles.label} htmlFor="username">
          Username
        </label>
        <input
          id="username"
          style={loginStyles.input}
          value={user}
          onChange={(e) => setUser(e.target.value)}
          autoComplete="username"
          placeholder="admin"
        />

        <label style={loginStyles.label} htmlFor="password">
          Password
        </label>
        <input
          id="password"
          type="password"
          style={loginStyles.input}
          value={pass}
          onChange={(e) => setPass(e.target.value)}
          autoComplete="current-password"
          placeholder="••••••••"
        />

        <button
          type="submit"
          style={{
            ...loginStyles.button,
            opacity: loading ? 0.7 : 1,
          }}
          disabled={loading}
        >
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
