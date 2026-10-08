import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { MainLayout } from './components/Layout';
import { ErrorBoundary } from './components/common';
import { store } from './store/store';

// Pages
import { Dashboard } from './pages/Dashboard';
import { ComparisonPage } from './pages/ComparisonPage';
import { ReportsPage } from './pages/ReportsPage';
import { ChatPage } from './pages/ChatPage';

// Styles
import './styles/index.css';

function App() {
  return (
    <ErrorBoundary>
      <Provider store={store}>
        <BrowserRouter>
          <MainLayout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/comparison" element={<ComparisonPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/chat" element={<ChatPage />} />
            </Routes>
          </MainLayout>
        </BrowserRouter>
      </Provider>
    </ErrorBoundary>
  );
}

export default App;
