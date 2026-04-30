export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceAttribution[];
  chartData?: ChartPayload;
  insights?: Insight[];
  toolTrace?: ToolTraceEntry[];
  timestamp: Date;
}

export interface SourceAttribution {
  sourceType: "sql" | "pdf" | "csv";
  sourceName: string;
  detail: string;
}

export interface ChartPayload {
  chartType: "bar" | "line" | "pie";
  title: string;
  labels: string[];
  datasets: ChartDataset[];
}

export interface ChartDataset {
  label: string;
  values: number[];
}

export interface Insight {
  metricName: string;
  metricValue: string;
  description: string;
}

export interface ToolTraceEntry {
  toolName: string;
  inputParameters: Record<string, unknown>;
  outputSummary: string;
  executionDurationMs: number;
}

export interface Filters {
  timePeriod?: { startDate: string; endDate: string };
  genres?: string[];
  regions?: string[];
}

export interface ErrorResponse {
  errorCode: string;
  message: string;
  correlationId: string;
}

export interface AuthToken {
  accessToken: string;
  tokenType: string;
}
