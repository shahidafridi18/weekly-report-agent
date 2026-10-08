import React, { useState } from 'react';
import { useReports } from '../../hooks';
import { useAppSelector } from '../../hooks';
import { Button } from '../common';
import { Download, X, FileText, FileSpreadsheet } from 'lucide-react';
import { GenerateReportRequest } from '../../types';
import { API_BASE_URL } from '../../utils/constants';

interface ReportGeneratorProps {
  onReportGenerated?: () => void;
}

export const ReportGenerator: React.FC<ReportGeneratorProps> = ({ onReportGenerated }) => {
  const { results, request: comparisonRequest } = useAppSelector(state => state.comparison);
  const { generateReport, loading } = useReports();
  const [reportFormat, setReportFormat] = useState<'pdf' | 'xlsx' | 'both'>('both');

  const handleGenerate = async () => {
    if (!results || !comparisonRequest) return;

    const request: GenerateReportRequest = {
      ...comparisonRequest,
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
  const { reports, deleteReport } = useReports();

  if (reports.length === 0) {
    return (
      <div className="bg-pale-blue border border-mid-grey rounded-lg p-6 text-center">
        <FileText className="w-12 h-12 text-mid-grey mx-auto mb-3" />
        <p className="text-dark-grey">No reports generated in this browser session yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {reports.map(report => {
        const Icon = report.format === 'pdf' ? FileText : FileSpreadsheet;
        return (
          <div key={report.report_id} className="rounded-xl border border-mid-grey bg-white p-4 shadow-sm sm:p-5">
            <div className="flex min-w-0 flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-start gap-3">
                <div className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-lg bg-light-blue text-blue">
                  <Icon className="h-6 w-6" />
                </div>
                <div className="min-w-0">
                  <p className="break-all text-sm font-semibold leading-6 text-navy">{report.filename}</p>
                  <p className="mt-1 text-xs text-dark-grey">{report.format.toUpperCase()} report · Generated this session</p>
                </div>
              </div>
              <div className="flex flex-shrink-0 items-center gap-2 sm:flex-col sm:items-stretch xl:flex-row">
                <a
                  href={`${API_BASE_URL}${report.download_url}?filename=${encodeURIComponent(report.filename)}`}
                  download={report.filename}
                  className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg bg-blue px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-navy focus:outline-none focus:ring-2 focus:ring-blue sm:flex-none"
                  aria-label={`Download ${report.filename}`}
                >
                  <Download className="h-4 w-4" /> Download
                </a>
                <button type="button" onClick={() => deleteReport(report.report_id)}
                  className="inline-flex items-center justify-center rounded-lg border border-mid-grey px-3 py-2.5 text-dark-grey hover:bg-pale-blue focus:outline-none focus:ring-2 focus:ring-blue"
                  title="Remove from this page (does not delete the saved report)" aria-label={`Remove ${report.filename} from list`}>
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
