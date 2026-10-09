// Constants used throughout the application

export const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT || '30000', 10);
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const DEFAULT_KEY_COLUMNS = ['SIREN', 'Unique Identifier'];

export const MOVEMENT_THRESHOLD_DEFAULT = 20.0;
export const MINIMUM_ABSOLUTE_CHANGE_DEFAULT = 0.0;

export const REPORT_FORMATS = ['pdf', 'xlsx', 'both'] as const;

export const CHAT_PLACEHOLDER = 'Ask about the analysis... (e.g., "Show me entities with highest variance")';

export const EMPTY_STATE_MESSAGES = {
  noFiles: 'No files found. Upload files to get started.',
  noResults: 'No results yet. Run a comparison to see analysis.',
  noChatMessages: 'No messages yet. Start asking questions about your data.',
  noReports: 'No reports generated yet.',
};

export const ERROR_MESSAGES = {
  fileUploadFailed: 'Failed to upload file. Please try again.',
  comparisonFailed: 'Comparison failed. Please check your inputs and try again.',
  reportGenerationFailed: 'Failed to generate report. Please try again.',
  chatFailed: 'Chat service unavailable. Please try again.',
  networkError: 'Network error. Please check your connection.',
  serverError: 'Server error. Please try again later.',
};

export const SUCCESS_MESSAGES = {
  fileUploaded: 'File uploaded successfully.',
  comparisonComplete: 'Comparison completed successfully.',
  reportGenerated: 'Report generated successfully.',
  reportDownloaded: 'Report downloaded successfully.',
};

export const LOADING_MESSAGES = {
  comparison: 'Running comparison analysis...',
  reportGeneration: 'Generating report...',
  downloading: 'Downloading report...',
  chat: 'Processing your message...',
};

export const TABLE_ROWS_PER_PAGE = 10;
export const DASHBOARD_ITEMS_PER_PAGE = 20;

export const COLOR_MAP = {
  increase: '#2E7D32',
  decrease: '#B3261E',
  stable: '#495057',
  primary: '#24364B',
  secondary: '#315F8C',
  accent: '#DCE8F2',
};

export const CHART_COLORS = [
  '#315F8C',
  '#2E7D32',
  '#B3261E',
  '#B26A00',
  '#24364B',
  '#DCE8F2',
];

export const DATE_FORMAT = 'MMM dd, yyyy HH:mm';
export const SHORT_DATE_FORMAT = 'MMM dd, yyyy';
