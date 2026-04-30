import { useEffect, useRef } from "react";
import type { Insight } from "../../types";

/* ------------------------------------------------------------------ */
/*  Accent colors by metric keyword                                    */
/* ------------------------------------------------------------------ */

const ACCENT_COLORS = [
  "#4f46e5", // indigo
  "#06b6d4", // cyan
  "#f59e0b", // amber
  "#22c55e", // green
  "#ef4444", // red
  "#8b5cf6", // violet
  "#ec4899", // pink
  "#14b8a6", // teal
];

function getAccentColor(metricName: string, index: number): string {
  const lower = metricName.toLowerCase();
  if (lower.includes("revenue") || lower.includes("spend") || lower.includes("cost"))
    return "#22c55e";
  if (lower.includes("rating") || lower.includes("score") || lower.includes("satisfaction"))
    return "#f59e0b";
  if (lower.includes("view") || lower.includes("watch") || lower.includes("engagement"))
    return "#06b6d4";
  if (lower.includes("growth") || lower.includes("trend") || lower.includes("increase"))
    return "#4f46e5";
  if (lower.includes("decline") || lower.includes("drop") || lower.includes("churn"))
    return "#ef4444";
  return ACCENT_COLORS[index % ACCENT_COLORS.length];
}

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: 16,
  },
  heading: {
    fontSize: 14,
    fontWeight: 600,
    color: "#1a1a2e",
    margin: "0 0 12px",
  },
  empty: {
    color: "#aaa",
    fontSize: 13,
    fontStyle: "italic",
    textAlign: "center" as const,
    padding: "24px 0",
  },
  card: {
    background: "#fff",
    border: "1px solid #eef0f4",
    borderRadius: 10,
    padding: "12px 14px 12px 18px",
    marginBottom: 10,
    position: "relative" as const,
    overflow: "hidden" as const,
    boxShadow: "0 1px 4px rgba(0,0,0,0.04)",
    transition: "box-shadow 0.2s ease, transform 0.2s ease",
  },
  accentBar: {
    position: "absolute" as const,
    left: 0,
    top: 0,
    bottom: 0,
    width: 4,
    borderRadius: "4px 0 0 4px",
  },
  metricName: {
    fontSize: 11,
    fontWeight: 600,
    color: "#6b7280",
    textTransform: "uppercase" as const,
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  metricValue: {
    fontSize: 22,
    fontWeight: 700,
    color: "#1a1a2e",
    marginBottom: 4,
  },
  description: {
    fontSize: 12,
    color: "#6b7280",
    lineHeight: 1.4,
  },
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

interface Props {
  insights: Insight[];
}

export default function InsightsPanel({ insights }: Props) {
  const prevCountRef = useRef(0);
  const isNewBatch = insights.length !== prevCountRef.current;

  useEffect(() => {
    prevCountRef.current = insights.length;
  }, [insights.length]);

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Insights</h3>

      {insights.length === 0 ? (
        <div style={styles.empty}>No insights yet</div>
      ) : (
        insights.map((insight, i) => {
          const accent = getAccentColor(insight.metricName, i);
          return (
            <div
              key={`${insight.metricName}-${i}`}
              className={isNewBatch ? "insight-card-animate" : ""}
              style={{
                ...styles.card,
                animationDelay: isNewBatch ? `${i * 0.07}s` : undefined,
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLDivElement).style.boxShadow =
                  "0 3px 12px rgba(0,0,0,0.08)";
                (e.currentTarget as HTMLDivElement).style.transform =
                  "translateY(-1px)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLDivElement).style.boxShadow =
                  "0 1px 4px rgba(0,0,0,0.04)";
                (e.currentTarget as HTMLDivElement).style.transform = "none";
              }}
            >
              <div style={{ ...styles.accentBar, background: accent }} />
              <div style={styles.metricName}>{insight.metricName}</div>
              <div style={styles.metricValue}>{insight.metricValue}</div>
              <div style={styles.description}>{insight.description}</div>
            </div>
          );
        })
      )}
    </div>
  );
}
