import { useCallback, useState } from "react";
import { AuthProvider, LoginForm, useAuth } from "./contexts/AuthContext";
import ChatInterface from "./components/ChatInterface/ChatInterface";
import FilterPanel from "./components/FilterPanel/FilterPanel";
import InsightsPanel from "./components/InsightsPanel/InsightsPanel";
import ChartRenderer from "./components/ChartRenderer/ChartRenderer";
import QueryHistory from "./components/QueryHistory/QueryHistory";
import { submitQuestion } from "./api/client";
import type { ChatMessage, ChartPayload, Filters, Insight } from "./types";
import "./App.css";

/* ------------------------------------------------------------------ */
/*  Collapsible sidebar section                                        */
/* ------------------------------------------------------------------ */

function SidebarSection({
  title,
  defaultOpen = true,
  children,
}: {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="sidebar-section">
      <div
        className="sidebar-section-header"
        onClick={() => setOpen((o) => !o)}
        role="button"
        tabIndex={0}
        aria-expanded={open}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            setOpen((o) => !o);
          }
        }}
      >
        <h3>{title}</h3>
        <span
          className={`sidebar-section-chevron${open ? "" : " collapsed"}`}
        >
          ▼
        </span>
      </div>
      <div className={`sidebar-section-body${open ? "" : " collapsed"}`}>
        {children}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Authenticated app shell                                            */
/* ------------------------------------------------------------------ */

function AppShell() {
  const { logout, username } = useAuth();

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [filters, setFilters] = useState<Filters>({});
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [chartData, setChartData] = useState<ChartPayload | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const queryCount = messages.filter((m) => m.role === "user").length;

  const handleSend = useCallback(
    async (question: string) => {
      // Add user message
      const userMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setLoading(true);
      setError(null);

      try {
        const activeFilters =
          filters.timePeriod || filters.genres?.length || filters.regions?.length
            ? filters
            : undefined;

        const response = await submitQuestion(question, activeFilters, sessionId);

        // Update session
        setSessionId(response.sessionId);

        // Add assistant message
        const assistantMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: response.answer,
          sources: response.sources,
          chartData: response.chartData,
          insights: response.insights,
          toolTrace: response.toolTrace,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMsg]);

        // Update insights and chart from latest response
        if (response.insights && response.insights.length > 0) {
          setInsights(response.insights);
        }
        if (response.chartData) {
          setChartData(response.chartData);
        }
      } catch (err: unknown) {
        const message =
          err instanceof Error ? err.message : "An error occurred";
        setError(message);
      } finally {
        setLoading(false);
      }
    },
    [filters, sessionId]
  );

  return (
    <>
      <header className="app-header">
        <div className="app-header-left">
          <h1>🎬 AI Insights Assistant</h1>
          <div className="app-header-status">
            <span className="app-header-status-dot" />
            Connected
          </div>
        </div>
        <div className="app-header-right">
          {queryCount > 0 && (
            <span style={{ fontSize: 12, color: "rgba(255,255,255,0.5)" }}>
              {queryCount} {queryCount === 1 ? "query" : "queries"}
            </span>
          )}
          <div className="app-header-user">
            <div className="app-header-avatar">
              {(username || "A").charAt(0).toUpperCase()}
            </div>
            <span>{username || "User"}</span>
          </div>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      {error && (
        <div className="app-error">
          <span>{error}</span>
          <button onClick={() => setError(null)} aria-label="Dismiss error">
            ×
          </button>
        </div>
      )}

      <div className="app-layout">
        {/* Left sidebar */}
        <aside className="app-sidebar">
          <SidebarSection title="Filters">
            <FilterPanel filters={filters} onChange={setFilters} />
          </SidebarSection>
          <hr className="app-sidebar-divider" />
          <SidebarSection title="Query History">
            <QueryHistory messages={messages} />
          </SidebarSection>
        </aside>

        {/* Center: Chat */}
        <main className="app-main">
          <ChatInterface
            messages={messages}
            onSend={handleSend}
            loading={loading}
          />
          <div className="app-footer">
            <span className="app-footer-dot" />
            <span>Powered by AI</span>
            <span style={{ margin: "0 4px", color: "#d1d5db" }}>·</span>
            <span>SQL + PDF + CSV multi-source retrieval</span>
            <span style={{ margin: "0 4px", color: "#d1d5db" }}>·</span>
            <span>Tool-based architecture</span>
          </div>
        </main>

        {/* Right panel */}
        <aside className="app-right">
          <InsightsPanel insights={insights} />
          <hr className="app-right-divider" />
          <ChartRenderer chartData={chartData} />
        </aside>
      </div>
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  Root App with auth gate                                            */
/* ------------------------------------------------------------------ */

function App() {
  return (
    <AuthProvider>
      <AuthGate />
    </AuthProvider>
  );
}

function AuthGate() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <AppShell /> : <LoginForm />;
}

export default App;
