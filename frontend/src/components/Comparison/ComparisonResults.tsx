import React from 'react';
import { ComparisonAnalysis } from '../../types';
import { formatNumber, formatPercentage } from '../../utils/formatters';

interface ComparisonResultsProps {
  analysis: ComparisonAnalysis;
}

export const ComparisonResults: React.FC<ComparisonResultsProps> = ({ analysis }) => {
  const { row_summary, metric_summary } = analysis;

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {[
          { label: 'Previous Rows', value: row_summary.previous_rows },
          { label: 'Current Rows', value: row_summary.current_rows },
          { label: 'Matched', value: row_summary.matched_rows },
          { label: 'New', value: row_summary.new_rows },
          { label: 'Removed', value: row_summary.removed_rows },
        ].map(stat => (
          <div key={stat.label} className="bg-light-blue rounded-lg p-4 text-center">
            <p className="text-sm text-dark-grey mb-1">{stat.label}</p>
            <p className="text-2xl font-bold text-navy">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Metrics Summary */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-navy mb-4">Key Metrics Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(metric_summary).map(([metric, values]) => (
            <div key={metric} className="border border-mid-grey rounded-lg p-4">
              <h4 className="font-semibold text-navy mb-2">{metric}</h4>
              <div className="space-y-1 text-sm text-dark-grey">
                <p>Previous: <span className="font-semibold">{formatNumber(values.previous_total)}</span></p>
                <p>Current: <span className="font-semibold">{formatNumber(values.current_total)}</span></p>
                <p>Change: <span className={values.absolute_change > 0 ? 'text-success' : 'text-danger'}>
                  {formatNumber(values.absolute_change)}
                </span></p>
                <p>Percentage: <span className={values.percentage_change > 0 ? 'text-success font-semibold' : 'text-danger font-semibold'}>
                  {formatPercentage(values.percentage_change)}
                </span></p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
