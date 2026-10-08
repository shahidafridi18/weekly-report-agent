// Types for API responses and data structures

export interface ColumnInfo {
  key_columns: string[];
  numerical_columns: string[];
}

export interface RowSummary {
  previous_rows: number;
  current_rows: number;
  matched_rows: number;
  new_rows: number;
  removed_rows: number;
}

export interface MetricValues {
  previous_total: number;
  current_total: number;
  absolute_change: number;
  percentage_change: number;
  direction: 'increase' | 'decrease' | 'stable';
}

export interface MetricSummary {
  [metricName: string]: MetricValues;
}

export interface MovementBridgeItem {
  metric: string;
  matched_entity_change: number;
  new_entity_impact: number;
  removed_entity_impact: number;
  explained_change: number;
  actual_total_change: number;
}

export interface Entity {
  [key: string]: string | number;
}

export interface VarianceRecord {
  [key: string]: any;
}

export interface NewEntity {
  entity: Entity;
  values: Record<string, number>;
}

export interface RemovedEntity {
  entity: Entity;
  previous_values: Record<string, number>;
}

export interface MajorMovement {
  entity: Entity;
  metric: string;
  previous_value: number;
  current_value: number;
  absolute_change: number;
  percentage_change: number;
  direction: 'increase' | 'decrease' | 'stable';
}

export interface ZeroTransition {
  entity: Entity;
  metric: string;
  previous_value: number;
  current_value: number;
  transition: string;
}

export interface ComparisonAnalysis {
  columns: ColumnInfo;
  row_summary: RowSummary;
  metric_summary: MetricSummary;
  movement_bridge: Record<string, MovementBridgeItem>;
  variance_data: VarianceRecord[];
  new_entities: NewEntity[];
  removed_entities: RemovedEntity[];
  major_movements: MajorMovement[];
  zero_transitions: ZeroTransition[];
}

export interface ComparisonResponse extends ComparisonAnalysis {
  ai_insights?: string;
}

export interface Report {
  id: string;
  format: 'pdf' | 'xlsx' | 'both';
  name: string;
  created_at: string;
  file_size?: number;
  previous_file: string;
  current_file: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatResponse {
  message: string;
  context?: string;
}

export interface CompareRequest {
  previous_file: string;
  current_file: string;
  key_columns: string[];
  movement_threshold_pct: number;
  minimum_absolute_change: number;
  generate_ai_insights: boolean;
  metrics?: string[];
}

export interface ReportRequest {
  compare_request: CompareRequest;
  report_format: 'pdf' | 'xlsx' | 'both';
}

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  modified: string;
}

export interface ApiError {
  detail: string | { message: string; candidates?: string[] };
}
