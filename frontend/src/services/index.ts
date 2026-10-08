// API Service for backend communication

import { apiClient } from '../utils/api';
import {
  ComparisonAnalysis,
  ComparisonResponse,
  ChatResponse,
  Report,
  FileInfo,
  CompareRequest,
  ReportRequest,
} from '../types';

class ComparisonService {
  async compareFiles(request: CompareRequest): Promise<ComparisonResponse> {
    const response = await apiClient.post<ComparisonResponse>(
      '/api/agent/compare',
      request
    );
    return response.data;
  }

  async analyzeFile(file: string, keyColumns: string[]): Promise<ComparisonAnalysis> {
    const response = await apiClient.post<ComparisonAnalysis>(
      '/api/agent/analyze',
      { file, key_columns: keyColumns }
    );
    return response.data;
  }
}

class ReportService {
  async generateReport(request: ReportRequest): Promise<Report> {
    const response = await apiClient.post<Report>(
      '/api/agent/reports',
      request
    );
    return response.data;
  }

  async downloadReport(format: 'pdf' | 'xlsx', reportId: string): Promise<Blob> {
    const response = await apiClient.get<Blob>(
      `/api/agent/reports/${format}/${reportId}`,
      { responseType: 'blob' }
    );
    return response.data;
  }

  async getReportsList(): Promise<Report[]> {
    // This would need to be implemented in the backend
    return [];
  }
}

class ChatService {
  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>(
      '/api/agent/chat',
      { message }
    );
    return response.data;
  }
}

class FileService {
  async listFiles(): Promise<FileInfo[]> {
    const response = await apiClient.get<FileInfo[]>(
      '/api/agent/files'
    );
    return response.data;
  }
}

// Export service instances
export const comparisonService = new ComparisonService();
export const reportService = new ReportService();
export const chatService = new ChatService();
export const fileService = new FileService();
