import { useAppDispatch, useAppSelector } from './useRedux';
import { setLoading, setError, addReport, removeReport } from '../store/slices/reportSlice';
import { reportService } from '../services';
import { ReportRequest } from '../types';
import toast from 'react-hot-toast';

export const useReports = () => {
  const dispatch = useAppDispatch();
  const { reports, currentReport, loading, error } = useAppSelector(
    state => state.reports
  );

  const generateReport = async (request: ReportRequest) => {
    dispatch(setLoading(true));
    dispatch(setError(null));
    try {
      const report = await reportService.generateReport(request);
      dispatch(addReport(report));
      toast.success('Report generated successfully');
      return report;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to generate report';
      dispatch(setError(errorMessage));
      toast.error(errorMessage);
      throw err;
    } finally {
      dispatch(setLoading(false));
    }
  };

  const downloadReport = async (format: 'pdf' | 'xlsx', reportId: string) => {
    dispatch(setLoading(true));
    try {
      const blob = await reportService.downloadReport(format, reportId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `report-${reportId}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success('Report downloaded successfully');
    } catch (err: any) {
      const errorMessage = 'Failed to download report';
      dispatch(setError(errorMessage));
      toast.error(errorMessage);
    } finally {
      dispatch(setLoading(false));
    }
  };

  const deleteReport = async (reportId: string) => {
    dispatch(removeReport(reportId));
  };

  return {
    reports,
    currentReport,
    loading,
    error,
    generateReport,
    downloadReport,
    deleteReport,
  };
};
