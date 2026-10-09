import React from 'react';
import { ComparisonAnalysis } from '../../types';
import { formatNumber, formatPercentage } from '../../utils/formatters';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MetricsTableProps {
  metrics: ComparisonAnalysis['metric_summary'];
}

export const MetricsTable: React.FC<MetricsTableProps> = ({ metrics }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <table className="w-full">
        <thead className="bg-navy text-white">
          <tr>
            <th className="px-6 py-3 text-left text-sm font-semibold">Metric</th>
            <th className="px-6 py-3 text-right text-sm font-semibold">Previous</th>
            <th className="px-6 py-3 text-right text-sm font-semibold">Current</th>
            <th className="px-6 py-3 text-right text-sm font-semibold">Change</th>
            <th className="px-6 py-3 text-right text-sm font-semibold">Change %</th>
            <th className="px-6 py-3 text-center text-sm font-semibold">Direction</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(metrics).map(([metricName, values], index) => (
            <tr
              key={metricName}
              className={index % 2 === 0 ? 'bg-pale-blue' : 'bg-white'}
            >
              <td className="px-6 py-3 text-sm font-medium text-navy">{metricName}</td>
              <td className="px-6 py-3 text-sm text-right text-dark-grey">
                {formatNumber(values.previous_total)}
              </td>
              <td className="px-6 py-3 text-sm text-right text-dark-grey">
                {formatNumber(values.current_total)}
              </td>
              <td className="px-6 py-3 text-sm text-right text-dark-grey">
                {formatNumber(values.absolute_change)}
              </td>
              <td className="px-6 py-3 text-sm text-right text-dark-grey">
                {formatPercentage(values.percentage_change)}
              </td>
              <td className="px-6 py-3 text-center">
                <div className="flex items-center justify-center">
                  {values.direction === 'increase' ? (
                    <>
                      <TrendingUp className="w-4 h-4 text-success" />
                      <span className="text-xs font-medium text-success ml-1">Up</span>
                    </>
                  ) : values.direction === 'decrease' ? (
                    <>
                      <TrendingDown className="w-4 h-4 text-danger" />
                      <span className="text-xs font-medium text-danger ml-1">Down</span>
                    </>
                  ) : (
                    <span className="text-xs font-medium text-dark-grey">Stable</span>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
