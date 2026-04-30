import { useState } from "react";
import type { ChatMessage } from "../../types";

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: "4px 16px 16px",
  },
  empty: {
    color: "#aaa",
    fontSize: 13,
    fontStyle: "italic",
    textAlign: "center" as const,
    padding: "16px 0",
  },
  item: {
    padding: "8px 10px",
    borderRadius: 8,
    cursor: "pointer",
    marginBottom: 4,
    transition: "background 0.15s, border-color 0.15s",
    border: "1px solid transparent",
    display: "flex",
    gap: 8,
    alignItems: "flex-start",
  },
  itemHover: {
    background: "#f3f4f6",
    border: "1px solid #e5e7eb",
  },
  number: {
    fontSize: 11,
    fontWeight: 700,
    color: "#a5b4fc",
    background: "#eef2ff",
    borderRadius: 6,
    minWidth: 22,
    height: 22,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    marginTop: 1,
  },
  itemContent: {
    flex: 1,
    minWidth: 0,
  },
  questionRow: {
    display: "flex",
    alignItems: "center",
    gap: 6,
  },
  question: {
    fontSize: 13,
    color: "#1a1a2e",
    fontWeight: 500,
    overflow: "hidden" as const,
    textOverflow: "ellipsis" as const,
    whiteSpace: "nowrap" as const,
    flex: 1,
    minWidth: 0,
  },
  expandIcon: {
    fontSize: 10,
    color: "#9ca3af",
    flexShrink: 0,
    transition: "transform 0.2s ease",
  },
  timestamp: {
    fontSize: 11,
    color: "#9ca3af",
    marginTop: 2,
  },
  traceContainer: {
    marginTop: 8,
    marginLeft: 30,
    padding: "8px 10px",
    background: "#f9fafb",
    borderRadius: 8,
    border: "1px solid #eef0f4",
  },
  traceTitle: {
    fontSize: 11,
    fontWeight: 600,
    color: "#6b7280",
    marginBottom: 6,
    textTransform: "uppercase" as const,
    letterSpacing: 0.5,
  },
  traceItem: {
    fontSize: 12,
    color: "#374151",
    padding: "4px 0",
    borderBottom: "1px solid #f3f4f6",
  },
  toolName: {
    fontWeight: 600,
    color: "#4f46e5",
  },
  duration: {
    color: "#9ca3af",
    fontSize: 11,
    marginLeft: 8,
  },
  summary: {
    fontSize: 11,
    color: "#6b7280",
    marginTop: 2,
  },
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

interface Props {
  messages: ChatMessage[];
}

export default function QueryHistory({ messages }: Props) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  // Only show user messages (queries)
  const queries = messages.filter((m) => m.role === "user");
  // Map user message id to the next assistant message (for tool trace)
  const responseMap = new Map<string, ChatMessage>();
  for (let i = 0; i < messages.length; i++) {
    if (messages[i].role === "user" && i + 1 < messages.length && messages[i + 1].role === "assistant") {
      responseMap.set(messages[i].id, messages[i + 1]);
    }
  }

  return (
    <div style={styles.container}>
      {queries.length === 0 ? (
        <div style={styles.empty}>No queries yet</div>
      ) : (
        queries.map((q, idx) => {
          const isExpanded = expandedId === q.id;
          const response = responseMap.get(q.id);

          return (
            <div key={q.id}>
              <div
                style={{
                  ...styles.item,
                  ...(isExpanded ? styles.itemHover : {}),
                }}
                onClick={() => setExpandedId(isExpanded ? null : q.id)}
                onMouseEnter={(e) => {
                  if (!isExpanded)
                    (e.currentTarget as HTMLDivElement).style.background =
                      "#f9fafb";
                }}
                onMouseLeave={(e) => {
                  if (!isExpanded)
                    (e.currentTarget as HTMLDivElement).style.background = "";
                }}
                role="button"
                tabIndex={0}
                aria-expanded={isExpanded}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    setExpandedId(isExpanded ? null : q.id);
                  }
                }}
              >
                <div style={styles.number}>{idx + 1}</div>
                <div style={styles.itemContent}>
                  <div style={styles.questionRow}>
                    <div style={styles.question}>{q.content}</div>
                    <span
                      style={{
                        ...styles.expandIcon,
                        transform: isExpanded ? "rotate(90deg)" : "rotate(0deg)",
                      }}
                    >
                      ▶
                    </span>
                  </div>
                  <div style={styles.timestamp}>
                    {q.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>

              {isExpanded && response?.toolTrace && response.toolTrace.length > 0 && (
                <div style={styles.traceContainer}>
                  <div style={styles.traceTitle}>Tool Trace</div>
                  {response.toolTrace.map((t, i) => (
                    <div key={i} style={styles.traceItem}>
                      <span style={styles.toolName}>{t.toolName}</span>
                      <span style={styles.duration}>
                        {t.executionDurationMs.toFixed(0)}ms
                      </span>
                      <div style={styles.summary}>{t.outputSummary}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}
