import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { ChartPayload } from "../../types";

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const COLORS = [
  "#4f46e5",
  "#06b6d4",
  "#f59e0b",
  "#ef4444",
  "#22c55e",
  "#8b5cf6",
  "#ec4899",
  "#14b8a6",
];

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
  cardWrapper: {
    background: "#fff",
    borderRadius: 12,
    border: "1px solid #eef0f4",
    boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
    padding: "16px 12px 12px",
    transition: "box-shadow 0.2s ease",
  },
  title: {
    fontSize: 13,
    fontWeight: 600,
    color: "#374151",
    textAlign: "center" as const,
    marginBottom: 12,
  },
  emptyState: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    justifyContent: "center",
    padding: "32px 0",
    gap: 8,
  },
  emptyIcon: {
    fontSize: 28,
    opacity: 0.5,
  },
  emptyText: {
    color: "#aaa",
    fontSize: 13,
    fontStyle: "italic",
  },
};

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function buildChartData(payload: ChartPayload) {
  // Transform labels + datasets into recharts-friendly array of objects
  return payload.labels.map((label, i) => {
    const point: Record<string, string | number> = { name: label };
    payload.datasets.forEach((ds) => {
      point[ds.label] = ds.values[i] ?? 0;
    });
    return point;
  });
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

interface Props {
  chartData: ChartPayload | null;
}

export default function ChartRenderer({ chartData }: Props) {
  if (!chartData) {
    return (
      <div style={styles.container}>
        <h3 style={styles.heading}>Chart</h3>
        <div style={styles.emptyState}>
          <div style={styles.emptyIcon}>📊</div>
          <div style={styles.emptyText}>No chart data available</div>
        </div>
      </div>
    );
  }

  // Validate data
  if (
    !chartData.labels ||
    chartData.labels.length === 0 ||
    !chartData.datasets ||
    chartData.datasets.length === 0
  ) {
    return (
      <div style={styles.container}>
        <h3 style={styles.heading}>Chart</h3>
        <div style={styles.emptyState}>
          <div style={styles.emptyIcon}>⚠️</div>
          <div style={styles.emptyText}>Chart data is incomplete or malformed</div>
        </div>
      </div>
    );
  }

  const data = buildChartData(chartData);

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Chart</h3>
      <div style={styles.cardWrapper}>
        <div style={styles.title}>{chartData.title}</div>

        <ResponsiveContainer width="100%" height={260}>
          {chartData.chartType === "bar" ? (
            <BarChart data={data}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              {chartData.datasets.map((ds, i) => (
                <Bar
                  key={ds.label}
                  dataKey={ds.label}
                  fill={COLORS[i % COLORS.length]}
                />
              ))}
            </BarChart>
          ) : chartData.chartType === "line" ? (
            <LineChart data={data}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              {chartData.datasets.map((ds, i) => (
                <Line
                  key={ds.label}
                  type="monotone"
                  dataKey={ds.label}
                  stroke={COLORS[i % COLORS.length]}
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              ))}
            </LineChart>
          ) : (
            <PieChart>
              <Pie
                data={data.map((d, i) => ({
                  name: d.name,
                  value: d[chartData.datasets[0].label] as number,
                  fill: COLORS[i % COLORS.length],
                }))}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={90}
                label={({ name }) => name}
              >
                {data.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
