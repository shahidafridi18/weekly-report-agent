import { configureStore } from '@reduxjs/toolkit';
import comparisonReducer from './slices/comparisonSlice';
import reportReducer from './slices/reportSlice';
import chatReducer from './slices/chatSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    comparison: comparisonReducer,
    reports: reportReducer,
    chat: chatReducer,
    ui: uiReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
