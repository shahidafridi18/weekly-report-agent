import React, { useState } from 'react';
import { useReports } from '../../hooks';
import { useAppSelector } from '../../hooks';
import { Button } from '../common';
import { Download, Trash2, FileText } from 'lucide-react';
import { ReportRequest } from '../../types';

interface ReportGeneratorProps {
  onReportGenerated?: () => void;
}

export const ReportGenerator: React.FC<ReportGeneratorProps> = ({ onReportGenerated }) => {
  const { results } = useAppSelector(state => state.comparison);
  const { generateReport, loading } = useReports();
  const [reportFormat, setReportFormat] = useState<'pdf' | 'xlsx' | 'both'>('both');

  const handleGenerate = async () => {
    if (!results) return;

    const request: ReportRequest = {
      compare_request: {
        previous_file: 'file1', // These would come from comparison request
        current_file: 'file2',
        key_columns: results.columns.key_columns,
        movement_threshold_pct: 20,
        minimum_absolute_change: 0,
        generate_ai_insights: true,
      },
      report_format: reportFormat,
    };

    try {
      await generateReport(request);
      onReportGenerated?.();
    } catch (error) {
      console.error('Failed to generate report:', error);
    }
  };

  if (!results) {
    return (
      <div className="bg-pale-blue border border-mid-grey rounded-lg p-6 text-center">
        <p className="text-dark-grey">Run a comparison first to generate reports</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
      <h3 className="text-lg font-bold text-navy">Generate Report</h3>

      <div>
        <label className="block text-sm font-semibold text-navy mb-2">Report Format</label>
        <div className="grid grid-cols-3 gap-3">
          {(['pdf', 'xlsx', 'both'] as const).map(format => (
            <button
              key={format}
              onClick={() => setReportFormat(format)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                reportFormat === format
                  ? 'bg-blue text-white'
                  : 'bg-pale-blue text-dark-grey hover:bg-light-blue'
              }`}
            >
              {format.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <Button
        onClick={handleGenerate}
        variant="primary"
        fullWidth
        isLoading={loading}
      >
        <FileText className="w-4 h-4" />
        Generate Report
      </Button>
    </div>
  );
};

export const ReportHistory: React.FC = () => {
  const { reports, downloadReport, deleteReport, loading } = useReports();

  if (reports.length === 0) {
    return (
      <div className="bg-pale-blue border border-mid-grey rounded-lg p-6 text-center">
        <FileText className="w-12 h-12 text-mid-grey mx-auto mb-3" />
        <p className="text-dark-grey">No reports generated yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <table className="w-full">
        <thead className="bg-navy text-white">
          <tr>
            <th className="px-6 py-3 text-left text-sm font-semibold">Report</th>
            <th className="px-6 py-3 text-left text-sm font-semibold">Format</th>
            <th className="px-6 py-3 text-left text-sm font-semibold">Created</th>
            <th className="px-6 py-3 text-center text-sm font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((report, index) => (
            <tr key={report.id} className={index % 2 === 0 ? 'bg-pale-blue' : 'bg-white'}>
              <td className="px-6 py-3 text-sm text-navy font-medium">{report.name}</td>
              <td className="px-6 py-3 text-sm text-dark-grey">{report.format.toUpperCase()}</td>
              <td className="px-6 py-3 text-sm text-dark-grey">{report.created_at}</td>
              <td className="px-6 py-3 text-center space-x-2">
                <button
                  onClick={() => downloadReport(report.format as 'pdf' | 'xlsx', report.id)}
                  disabled={loading}
                  className="text-blue hover:text-navy disabled:text-mid-grey transition-colors"
                >
                  <Download className="w-5 h-5" />
                </button>
                <button
                  onClick={() => deleteReport(report.id)}
                  disabled={loading}
                  className="text-danger hover:text-red-700 disabled:text-mid-grey transition-colors"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
