import { useAppDispatch, useAppSelector } from './useRedux';
import { setRequest, setResults, setLoading, setError } from '../store/slices/comparisonSlice';
import { comparisonService } from '../services';
import { CompareRequest } from '../types';
import { getApiErrorMessage } from '../utils/api';

export const useComparison = () => {
  const dispatch = useAppDispatch();
  const { request, results, aiInsights, loading, error } = useAppSelector(
    state => state.comparison
  );

  const runComparison = async (compareRequest: CompareRequest) => {
    dispatch(setLoading(true));
    dispatch(setError(null));
    try {
      dispatch(setRequest(compareRequest));
      const response = await comparisonService.compareFiles(compareRequest);
      dispatch(setResults({
        results: response.analysis,
        insights: response.ai.insights || undefined,
      }));
    } catch (err: any) {
      const errorMessage = getApiErrorMessage(err, 'Failed to run comparison');
      dispatch(setError(errorMessage));
      throw err;
    }
  };

  return {
    request,
    results,
    aiInsights,
    loading,
    error,
    runComparison,
  };
};
