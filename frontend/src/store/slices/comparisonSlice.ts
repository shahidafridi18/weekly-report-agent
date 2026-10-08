import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ComparisonAnalysis, CompareRequest } from '../../types';

interface ComparisonState {
  request: CompareRequest | null;
  results: ComparisonAnalysis | null;
  aiInsights: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: ComparisonState = {
  request: null,
  results: null,
  aiInsights: null,
  loading: false,
  error: null,
};

const comparisonSlice = createSlice({
  name: 'comparison',
  initialState,
  reducers: {
    setRequest: (state, action: PayloadAction<CompareRequest>) => {
      state.request = action.payload;
    },
    setResults: (state, action: PayloadAction<{ results: ComparisonAnalysis; insights?: string }>) => {
      state.results = action.payload.results;
      state.aiInsights = action.payload.insights || null;
      state.loading = false;
      state.error = null;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.loading = false;
    },
    clearComparison: (state) => {
      state.request = null;
      state.results = null;
      state.aiInsights = null;
      state.error = null;
    },
  },
});

export const { setRequest, setResults, setLoading, setError, clearComparison } =
  comparisonSlice.actions;
export default comparisonSlice.reducer;
