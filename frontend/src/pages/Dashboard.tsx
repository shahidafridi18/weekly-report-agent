import React from 'react';
import { BarChart3, FileText, MessageSquare, TrendingUp } from 'lucide-react';
import { Button } from '../common';
import { useNavigate } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  const quickActions = [
    {
      icon: BarChart3,
      title: 'Run Comparison',
      description: 'Compare two weekly reports',
      action: () => navigate('/comparison'),
      color: 'bg-blue',
    },
    {
      icon: FileText,
      title: 'View Reports',
      description: 'Download generated reports',
      action: () => navigate('/reports'),
      color: 'bg-success',
    },
    {
      icon: MessageSquare,
      title: 'Chat',
      description: 'Ask AI questions about data',
      action: () => navigate('/chat'),
      color: 'bg-warning',
    },
    {
      icon: TrendingUp,
      title: 'Analytics',
      description: 'View detailed analytics',
      action: () => navigate('#'),
      color: 'bg-navy',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-navy to-blue text-white rounded-lg p-8 shadow-lg">
        <h1 className="text-3xl font-bold mb-2">Welcome to Weekly Report Agent</h1>
        <p className="text-blue-100">
          Upload files, run comparisons, and get AI-powered business insights
        </p>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold text-navy mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map(action => {
            const Icon = action.icon;
            return (
              <button
                key={action.title}
                onClick={action.action}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-all hover:-translate-y-1 text-left"
              >
                <div className={`${action.color} text-white rounded-lg w-12 h-12 flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="font-bold text-navy mb-1">{action.title}</h3>
                <p className="text-sm text-dark-grey">{action.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-navy mb-4">Getting Started</h2>
        <ol className="space-y-3 text-dark-grey">
          <li className="flex gap-3">
            <span className="font-bold text-blue">1.</span>
            <span>Upload or select two weekly Excel files with counterparty data</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-blue">2.</span>
            <span>Configure comparison parameters (key columns, thresholds)</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-blue">3.</span>
            <span>Run the comparison to see detailed analysis and AI insights</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-blue">4.</span>
            <span>Generate PDF or Excel reports for stakeholders</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-blue">5.</span>
            <span>Use the chat interface to ask follow-up questions about the data</span>
          </li>
        </ol>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-pale-blue rounded-lg p-6 border border-light-blue">
          <h3 className="font-bold text-navy mb-2">📊 Comparison Analysis</h3>
          <p className="text-sm text-dark-grey">
            Automatic entity matching, variance detection, and movement analysis
          </p>
        </div>
        <div className="bg-pale-blue rounded-lg p-6 border border-light-blue">
          <h3 className="font-bold text-navy mb-2">🤖 AI Insights</h3>
          <p className="text-sm text-dark-grey">
            Gemini-powered business insights and contextual analysis
          </p>
        </div>
        <div className="bg-pale-blue rounded-lg p-6 border border-light-blue">
          <h3 className="font-bold text-navy mb-2">📄 Report Generation</h3>
          <p className="text-sm text-dark-grey">
            Export results as PDF or Excel with charts and formatting
          </p>
        </div>
      </div>
    </div>
  );
};
