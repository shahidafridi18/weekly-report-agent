import React from 'react';
import { useAppSelector } from '../hooks';
import { ComparisonForm, ComparisonResults, MetricsTable } from '../components/Comparison';
import { ReportGenerator } from '../components/Reports';
import { Loading } from '../components/common';

export const ComparisonPage: React.FC = () => {
  const { results, aiInsights, loading, error } = useAppSelector(state => state.comparison);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-navy mb-2">Comparison Analysis</h1>
        <p className="text-dark-grey">Compare two weekly reports and get detailed analysis</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-danger text-danger rounded-lg p-4">
          {error}
        </div>
      )}

      {loading ? (
        <Loading message="Running comparison..." />
      ) : !results ? (
        <ComparisonForm onSuccess={() => window.scrollTo({ top: 0, behavior: 'smooth' })} />
      ) : (
        <>
          {/* Results */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-navy mb-6">Analysis Results</h2>
            <ComparisonResults analysis={results} />
          </div>

          {/* Metrics Table */}
          <div>
            <h2 className="text-2xl font-bold text-navy mb-4">Detailed Metrics</h2>
            <MetricsTable metrics={results.metric_summary} />
          </div>

          {/* AI Insights */}
          {aiInsights && (
            <div className="bg-light-blue border border-blue rounded-lg p-6">
              <h2 className="text-2xl font-bold text-navy mb-4">AI Business Insights</h2>
              <div className="prose prose-sm max-w-none text-dark-grey whitespace-pre-wrap">
                {aiInsights}
              </div>
            </div>
          )}

          {/* Report Generator */}
          <ReportGenerator />

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={() => {
                // Clear comparison
                window.location.reload();
              }}
              className="px-6 py-3 bg-pale-blue text-blue rounded-lg hover:bg-light-blue transition-colors font-medium"
            >
              New Comparison
            </button>
          </div>
        </>
      )}
    </div>
  );
};
