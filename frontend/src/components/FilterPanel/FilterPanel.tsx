import type { Filters } from "../../types";

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const GENRES = [
  "Action",
  "Comedy",
  "Drama",
  "Sci-Fi",
  "Thriller",
  "Horror",
  "Romance",
  "Animation",
];

const REGIONS = [
  "New York",
  "Los Angeles",
  "Chicago",
  "Houston",
  "Phoenix",
  "Philadelphia",
  "San Antonio",
  "San Diego",
];

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: "4px 16px 16px",
    fontSize: 13,
  },
  countBadge: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    minWidth: 20,
    height: 20,
    padding: "0 6px",
    borderRadius: 10,
    background: "#4f46e5",
    color: "#fff",
    fontSize: 11,
    fontWeight: 700,
    marginLeft: 8,
  },
  section: {
    marginBottom: 14,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: 600,
    color: "#6b7280",
    marginBottom: 6,
    textTransform: "uppercase" as const,
    letterSpacing: 0.5,
  },
  dateRow: {
    display: "flex",
    gap: 8,
    alignItems: "center",
  },
  dateInput: {
    flex: 1,
    padding: "6px 8px",
    border: "1px solid #d1d5db",
    borderRadius: 8,
    fontSize: 12,
    transition: "border-color 0.15s",
  },
  pillGrid: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 6,
  },
  pill: {
    display: "inline-flex",
    alignItems: "center",
    padding: "4px 12px",
    borderRadius: 16,
    fontSize: 12,
    fontWeight: 500,
    cursor: "pointer",
    border: "1px solid #e0e3eb",
    background: "#f9fafb",
    color: "#4b5563",
    transition: "all 0.15s ease",
    userSelect: "none" as const,
  },
  pillActive: {
    background: "#eef2ff",
    borderColor: "#a5b4fc",
    color: "#4338ca",
    fontWeight: 600,
  },
  badgeRow: {
    display: "flex",
    flexWrap: "wrap" as const,
    gap: 4,
    marginTop: 12,
  },
  badge: {
    display: "inline-flex",
    alignItems: "center",
    gap: 4,
    padding: "3px 10px",
    background: "#eef2ff",
    color: "#4338ca",
    borderRadius: 14,
    fontSize: 11,
    fontWeight: 500,
    border: "1px solid #c7d2fe",
  },
  badgeX: {
    cursor: "pointer",
    fontWeight: 700,
    marginLeft: 2,
    fontSize: 13,
    lineHeight: 1,
  },
  clearBtn: {
    marginTop: 8,
    padding: "5px 12px",
    background: "none",
    border: "1px solid #d1d5db",
    borderRadius: 8,
    fontSize: 12,
    color: "#666",
    cursor: "pointer",
    transition: "background 0.15s",
  },
};

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

interface Props {
  filters: Filters;
  onChange: (filters: Filters) => void;
}

export default function FilterPanel({ filters, onChange }: Props) {
  const activeCount =
    (filters.timePeriod ? 1 : 0) +
    (filters.genres?.length ?? 0) +
    (filters.regions?.length ?? 0);

  const toggleItem = (
    key: "genres" | "regions",
    value: string,
    checked: boolean
  ) => {
    const current = filters[key] ?? [];
    const next = checked
      ? [...current, value]
      : current.filter((v) => v !== value);
    onChange({ ...filters, [key]: next.length > 0 ? next : undefined });
  };

  const removeItem = (key: "genres" | "regions", value: string) => {
    const current = filters[key] ?? [];
    const next = current.filter((v) => v !== value);
    onChange({ ...filters, [key]: next.length > 0 ? next : undefined });
  };

  const clearAll = () => {
    onChange({});
  };

  return (
    <div style={styles.container}>
      {activeCount > 0 && <span style={styles.countBadge}>{activeCount}</span>}

      {/* Time Period */}
      <div style={styles.section}>
        <div style={styles.sectionTitle}>Time Period</div>
        <div style={styles.dateRow}>
          <input
            type="date"
            style={styles.dateInput}
            value={filters.timePeriod?.startDate ?? ""}
            onChange={(e) =>
              onChange({
                ...filters,
                timePeriod: e.target.value
                  ? {
                      startDate: e.target.value,
                      endDate: filters.timePeriod?.endDate ?? "",
                    }
                  : undefined,
              })
            }
            aria-label="Start date"
          />
          <span style={{ color: "#999", fontSize: 12 }}>to</span>
          <input
            type="date"
            style={styles.dateInput}
            value={filters.timePeriod?.endDate ?? ""}
            onChange={(e) =>
              onChange({
                ...filters,
                timePeriod: e.target.value
                  ? {
                      startDate: filters.timePeriod?.startDate ?? "",
                      endDate: e.target.value,
                    }
                  : undefined,
              })
            }
            aria-label="End date"
          />
        </div>
      </div>

      {/* Genre pills */}
      <div style={styles.section}>
        <div style={styles.sectionTitle}>Genre</div>
        <div style={styles.pillGrid}>
          {GENRES.map((g) => {
            const active = filters.genres?.includes(g) ?? false;
            return (
              <span
                key={g}
                style={{
                  ...styles.pill,
                  ...(active ? styles.pillActive : {}),
                }}
                onClick={() => toggleItem("genres", g, !active)}
                onMouseEnter={(e) => {
                  if (!active)
                    (e.currentTarget as HTMLSpanElement).style.borderColor =
                      "#a5b4fc";
                }}
                onMouseLeave={(e) => {
                  if (!active)
                    (e.currentTarget as HTMLSpanElement).style.borderColor =
                      "#e0e3eb";
                }}
                role="checkbox"
                aria-checked={active}
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    toggleItem("genres", g, !active);
                  }
                }}
              >
                {g}
              </span>
            );
          })}
        </div>
      </div>

      {/* Region pills */}
      <div style={styles.section}>
        <div style={styles.sectionTitle}>Region</div>
        <div style={styles.pillGrid}>
          {REGIONS.map((r) => {
            const active = filters.regions?.includes(r) ?? false;
            return (
              <span
                key={r}
                style={{
                  ...styles.pill,
                  ...(active ? styles.pillActive : {}),
                }}
                onClick={() => toggleItem("regions", r, !active)}
                onMouseEnter={(e) => {
                  if (!active)
                    (e.currentTarget as HTMLSpanElement).style.borderColor =
                      "#a5b4fc";
                }}
                onMouseLeave={(e) => {
                  if (!active)
                    (e.currentTarget as HTMLSpanElement).style.borderColor =
                      "#e0e3eb";
                }}
                role="checkbox"
                aria-checked={active}
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    toggleItem("regions", r, !active);
                  }
                }}
              >
                {r}
              </span>
            );
          })}
        </div>
      </div>

      {/* Active filter badges */}
      {activeCount > 0 && (
        <>
          <div style={styles.badgeRow}>
            {filters.timePeriod && (
              <span style={styles.badge}>
                📅 {filters.timePeriod.startDate || "…"} →{" "}
                {filters.timePeriod.endDate || "…"}
                <span
                  style={styles.badgeX}
                  onClick={() =>
                    onChange({ ...filters, timePeriod: undefined })
                  }
                  role="button"
                  aria-label="Remove time filter"
                >
                  ×
                </span>
              </span>
            )}
            {filters.genres?.map((g) => (
              <span key={g} style={styles.badge}>
                🎬 {g}
                <span
                  style={styles.badgeX}
                  onClick={() => removeItem("genres", g)}
                  role="button"
                  aria-label={`Remove ${g}`}
                >
                  ×
                </span>
              </span>
            ))}
            {filters.regions?.map((r) => (
              <span key={r} style={styles.badge}>
                📍 {r}
                <span
                  style={styles.badgeX}
                  onClick={() => removeItem("regions", r)}
                  role="button"
                  aria-label={`Remove ${r}`}
                >
                  ×
                </span>
              </span>
            ))}
          </div>
          <button
            style={styles.clearBtn}
            onClick={clearAll}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLButtonElement).style.background =
                "#f3f4f6";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLButtonElement).style.background = "none";
            }}
          >
            Clear all filters
          </button>
        </>
      )}
    </div>
  );
}
