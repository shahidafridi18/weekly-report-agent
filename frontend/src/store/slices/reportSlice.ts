import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Report } from '../../types';

interface ReportState {
  reports: Report[];
  currentReport: Report | null;
  loading: boolean;
  error: string | null;
  downloadProgress: number;
}

const initialState: ReportState = {
  reports: [],
  currentReport: null,
  loading: false,
  error: null,
  downloadProgress: 0,
};

const reportSlice = createSlice({
  name: 'reports',
  initialState,
  reducers: {
    setReports: (state, action: PayloadAction<Report[]>) => {
      state.reports = action.payload;
    },
    addReport: (state, action: PayloadAction<Report>) => {
      state.reports.unshift(action.payload);
      state.currentReport = action.payload;
    },
    setCurrentReport: (state, action: PayloadAction<Report>) => {
      state.currentReport = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setDownloadProgress: (state, action: PayloadAction<number>) => {
      state.downloadProgress = action.payload;
    },
    removeReport: (state, action: PayloadAction<string>) => {
      state.reports = state.reports.filter(r => r.id !== action.payload);
      if (state.currentReport?.id === action.payload) {
        state.currentReport = null;
      }
    },
    clearReports: (state) => {
      state.reports = [];
      state.currentReport = null;
      state.error = null;
    },
  },
});

export const {
  setReports,
  addReport,
  setCurrentReport,
  setLoading,
  setError,
  setDownloadProgress,
  removeReport,
  clearReports,
} = reportSlice.actions;
export default reportSlice.reducer;
