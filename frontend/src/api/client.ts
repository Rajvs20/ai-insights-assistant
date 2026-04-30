import axios from "axios";
import type {
  AuthToken,
  ChatMessage,
  ChartPayload,
  Filters,
  Insight,
  SourceAttribution,
  ToolTraceEntry,
} from "../types";

const TOKEN_KEY = "auth_token";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
});

// Auto-include JWT token in Authorization header
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 by clearing token and redirecting to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

/* ------------------------------------------------------------------ */
/*  snake_case → camelCase helpers                                     */
/* ------------------------------------------------------------------ */

function mapSource(s: Record<string, unknown>): SourceAttribution {
  return {
    sourceType: s.source_type as SourceAttribution["sourceType"],
    sourceName: s.source_name as string,
    detail: s.detail as string,
  };
}

function mapChartDataset(d: Record<string, unknown>) {
  return { label: d.label as string, values: d.values as number[] };
}

function mapChartData(c: Record<string, unknown> | null): ChartPayload | undefined {
  if (!c) return undefined;
  return {
    chartType: c.chart_type as ChartPayload["chartType"],
    title: c.title as string,
    labels: c.labels as string[],
    datasets: (c.datasets as Record<string, unknown>[]).map(mapChartDataset),
  };
}

function mapInsight(i: Record<string, unknown>): Insight {
  return {
    metricName: i.metric_name as string,
    metricValue: i.metric_value as string,
    description: i.description as string,
  };
}

function mapToolTrace(t: Record<string, unknown>): ToolTraceEntry {
  return {
    toolName: t.tool_name as string,
    inputParameters: t.input_parameters as Record<string, unknown>,
    outputSummary: t.output_summary as string,
    executionDurationMs: t.execution_duration_ms as number,
  };
}

/* ------------------------------------------------------------------ */
/*  API functions                                                      */
/* ------------------------------------------------------------------ */

export interface ChatResponse {
  answer: string;
  sources: SourceAttribution[];
  chartData?: ChartPayload;
  insights?: Insight[];
  toolTrace: ToolTraceEntry[];
  sessionId: string;
  correlationId: string;
}

export async function login(
  username: string,
  password: string
): Promise<AuthToken> {
  const { data } = await api.post("/api/auth/login", { username, password });
  return {
    accessToken: data.access_token,
    tokenType: data.token_type,
  };
}

export async function submitQuestion(
  question: string,
  filters?: Filters,
  sessionId?: string
): Promise<ChatResponse> {
  // Convert camelCase filters to snake_case for the backend
  const backendFilters = filters
    ? {
        time_period: filters.timePeriod
          ? {
              start_date: filters.timePeriod.startDate,
              end_date: filters.timePeriod.endDate,
            }
          : undefined,
        genres: filters.genres,
        regions: filters.regions,
      }
    : undefined;

  const { data } = await api.post("/api/chat", {
    question,
    filters: backendFilters,
    session_id: sessionId,
  });

  return {
    answer: data.answer,
    sources: (data.sources ?? []).map(mapSource),
    chartData: mapChartData(data.chart_data),
    insights: data.insights?.map(mapInsight),
    toolTrace: (data.tool_trace ?? []).map(mapToolTrace),
    sessionId: data.session_id,
    correlationId: data.correlation_id,
  };
}

export async function getChatHistory(
  sessionId: string
): Promise<ChatMessage[]> {
  const { data } = await api.get(`/api/chat/history/${sessionId}`);
  // The backend may return an array of messages
  if (Array.isArray(data)) {
    return data.map(
      (msg: Record<string, unknown>, idx: number): ChatMessage => ({
        id: (msg.id as string) ?? String(idx),
        role: msg.role as "user" | "assistant",
        content: msg.content as string,
        sources: msg.sources
          ? (msg.sources as Record<string, unknown>[]).map(mapSource)
          : undefined,
        chartData: msg.chart_data
          ? mapChartData(msg.chart_data as Record<string, unknown>)
          : undefined,
        insights: msg.insights
          ? (msg.insights as Record<string, unknown>[]).map(mapInsight)
          : undefined,
        toolTrace: msg.tool_trace
          ? (msg.tool_trace as Record<string, unknown>[]).map(mapToolTrace)
          : undefined,
        timestamp: new Date((msg.timestamp as string) ?? Date.now()),
      })
    );
  }
  return [];
}

export interface DataSource {
  type: string;
  name: string;
  details: Record<string, unknown>;
}

export async function getDataSources(): Promise<DataSource[]> {
  const { data } = await api.get("/api/data/sources");
  return data as DataSource[];
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}
