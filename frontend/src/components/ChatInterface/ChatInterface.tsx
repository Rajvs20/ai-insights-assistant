import { useEffect, useRef, useState, type FormEvent } from "react";
import Markdown from "react-markdown";
import type { ChatMessage, SourceAttribution } from "../../types";

/* ------------------------------------------------------------------ */
/*  Suggested questions                                                */
/* ------------------------------------------------------------------ */

const SUGGESTED_QUESTIONS = [
  "Which titles performed best in 2025?",
  "Why is Stellar Run trending?",
  "Compare Dark Orbit vs Last Kingdom",
  "Which city had the strongest engagement?",
  "What explains weak comedy performance?",
  "What recommendations for leadership?",
];

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100%",
    background: "transparent",
  },
  thread: {
    flex: 1,
    overflowY: "auto",
    padding: "20px 24px",
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  /* Empty state */
  emptyState: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    marginTop: 48,
    gap: 8,
  },
  emptyIcon: {
    fontSize: 36,
    marginBottom: 4,
    opacity: 0.7,
  },
  emptyTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: "#1a1a2e",
    margin: 0,
  },
  emptySubtitle: {
    fontSize: 13,
    color: "#9ca3af",
    margin: "0 0 20px",
  },
  chipsContainer: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 8,
    justifyContent: "center",
    maxWidth: 560,
    padding: "0 16px",
  },
  chip: {
    padding: "8px 16px",
    background: "#fff",
    border: "1px solid #e0e3eb",
    borderRadius: 20,
    fontSize: 13,
    color: "#4f46e5",
    cursor: "pointer",
    transition: "all 0.18s ease",
    fontWeight: 500,
    lineHeight: 1.4,
    boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
  },
  /* Bubbles */
  bubbleUser: {
    alignSelf: "flex-end",
    background: "linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)",
    color: "#fff",
    borderRadius: "18px 18px 4px 18px",
    padding: "12px 18px",
    maxWidth: "75%",
    fontSize: 14,
    lineHeight: 1.55,
    wordBreak: "break-word" as const,
    boxShadow: "0 2px 8px rgba(79, 70, 229, 0.18)",
  },
  bubbleAssistant: {
    alignSelf: "flex-start",
    background: "#fff",
    color: "#1a1a2e",
    borderRadius: "18px 18px 18px 4px",
    padding: "12px 18px",
    maxWidth: "85%",
    fontSize: 14,
    lineHeight: 1.6,
    wordBreak: "break-word" as const,
    boxShadow: "0 1px 6px rgba(0,0,0,0.06)",
    border: "1px solid #f0f0f4",
  },
  sourceBadge: {
    display: "inline-block",
    padding: "2px 8px",
    borderRadius: 12,
    fontSize: 11,
    fontWeight: 600,
    marginRight: 4,
    marginTop: 6,
    color: "#fff",
  },
  inputRow: {
    display: "flex",
    gap: 8,
    padding: "12px 24px",
    borderTop: "1px solid #e5e7eb",
    background: "#fff",
  },
  input: {
    flex: 1,
    padding: "10px 14px",
    border: "1px solid #d1d5db",
    borderRadius: 10,
    fontSize: 14,
    outline: "none",
    transition: "border-color 0.15s, box-shadow 0.15s",
  },
  sendBtn: {
    padding: "10px 20px",
    background: "linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)",
    color: "#fff",
    border: "none",
    borderRadius: 10,
    fontSize: 14,
    fontWeight: 600,
    cursor: "pointer",
    whiteSpace: "nowrap" as const,
    transition: "opacity 0.15s, box-shadow 0.15s",
    boxShadow: "0 2px 6px rgba(79, 70, 229, 0.2)",
  },
  spinner: {
    alignSelf: "flex-start",
    padding: "12px 18px",
    color: "#6b7280",
    fontSize: 14,
    fontStyle: "italic",
    background: "#fff",
    borderRadius: "18px 18px 18px 4px",
    boxShadow: "0 1px 6px rgba(0,0,0,0.06)",
    border: "1px solid #f0f0f4",
  },
  charCount: {
    fontSize: 11,
    color: "#999",
    alignSelf: "center",
  },
};

const SOURCE_COLORS: Record<string, string> = {
  sql: "#3b82f6",
  pdf: "#22c55e",
  csv: "#f97316",
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

interface Props {
  messages: ChatMessage[];
  onSend: (question: string) => void;
  loading: boolean;
}

export default function ChatInterface({ messages, onSend, loading }: Props) {
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const threadRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (threadRef.current) {
      threadRef.current.scrollTop = threadRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) {
      setError("Please enter a question");
      return;
    }
    if (trimmed.length > 2000) {
      setError("Question must be 2000 characters or less");
      return;
    }
    setError("");
    onSend(trimmed);
    setInput("");
  };

  const handleChipClick = (question: string) => {
    if (loading) return;
    onSend(question);
  };

  const renderSources = (sources?: SourceAttribution[]) => {
    if (!sources || sources.length === 0) return null;
    return (
      <div style={{ marginTop: 6 }}>
        {sources.map((s, i) => (
          <span
            key={i}
            style={{
              ...styles.sourceBadge,
              background: SOURCE_COLORS[s.sourceType] ?? "#6b7280",
            }}
            title={s.detail}
          >
            {s.sourceType.toUpperCase()}: {s.sourceName}
          </span>
        ))}
      </div>
    );
  };

  return (
    <div style={styles.container}>
      <div ref={threadRef} style={styles.thread}>
        {messages.length === 0 && (
          <div style={styles.emptyState}>
            <div style={styles.emptyIcon}>💬</div>
            <p style={styles.emptyTitle}>Ask a question about your data</p>
            <p style={styles.emptySubtitle}>
              Movies, viewers, marketing, regional performance and more
            </p>
            <div style={styles.chipsContainer}>
              {SUGGESTED_QUESTIONS.map((q) => (
                <button
                  key={q}
                  style={styles.chip}
                  onClick={() => handleChipClick(q)}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLButtonElement).style.background =
                      "#f0eeff";
                    (e.currentTarget as HTMLButtonElement).style.borderColor =
                      "#c7d2fe";
                    (e.currentTarget as HTMLButtonElement).style.boxShadow =
                      "0 2px 8px rgba(79,70,229,0.10)";
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLButtonElement).style.background =
                      "#fff";
                    (e.currentTarget as HTMLButtonElement).style.borderColor =
                      "#e0e3eb";
                    (e.currentTarget as HTMLButtonElement).style.boxShadow =
                      "0 1px 3px rgba(0,0,0,0.04)";
                  }}
                  disabled={loading}
                  type="button"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className="message-animate">
            <div
              style={
                msg.role === "user"
                  ? styles.bubbleUser
                  : styles.bubbleAssistant
              }
            >
              {msg.role === "assistant" ? (
                <Markdown>{msg.content}</Markdown>
              ) : (
                msg.content
              )}
            </div>
            {msg.role === "assistant" && (
              <div style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 4, flexWrap: "wrap" }}>
                {renderSources(msg.sources)}
                <span style={{ fontSize: 10, color: "#b0b3c1", marginLeft: "auto" }}>
                  {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={styles.spinner} className="message-animate">
            <span style={{ display: "inline-flex", gap: 4, alignItems: "center" }}>
              <span style={{ fontSize: 16 }}>🤔</span>
              Analyzing your data
              <span className="typing-dots">
                <span style={{ animation: "pulse 1.4s ease-in-out infinite", animationDelay: "0s" }}>.</span>
                <span style={{ animation: "pulse 1.4s ease-in-out infinite", animationDelay: "0.2s" }}>.</span>
                <span style={{ animation: "pulse 1.4s ease-in-out infinite", animationDelay: "0.4s" }}>.</span>
              </span>
            </span>
          </div>
        )}
      </div>

      <form style={styles.inputRow} onSubmit={handleSubmit}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            if (error) setError("");
          }}
          onFocus={(e) => {
            (e.currentTarget as HTMLInputElement).style.borderColor = "#a5b4fc";
            (e.currentTarget as HTMLInputElement).style.boxShadow =
              "0 0 0 3px rgba(79,70,229,0.08)";
          }}
          onBlur={(e) => {
            (e.currentTarget as HTMLInputElement).style.borderColor = "#d1d5db";
            (e.currentTarget as HTMLInputElement).style.boxShadow = "none";
          }}
          placeholder="Ask about movies, viewers, marketing…"
          disabled={loading}
          maxLength={2000}
          aria-label="Question input"
        />
        <span style={styles.charCount}>{input.length}/2000</span>
        <button
          type="submit"
          style={{ ...styles.sendBtn, opacity: loading ? 0.6 : 1 }}
          disabled={loading}
        >
          Send
        </button>
      </form>
      {error && (
        <div
          style={{
            color: "#e53e3e",
            fontSize: 12,
            padding: "0 24px 8px",
            background: "#fff",
          }}
        >
          {error}
        </div>
      )}
    </div>
  );
}
