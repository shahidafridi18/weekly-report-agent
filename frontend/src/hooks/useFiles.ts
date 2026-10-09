import { useState, useCallback } from 'react';
import { fileService } from '../services';
import { FileInfo } from '../types';
import { getApiErrorMessage } from '../utils/api';

export const useFiles = () => {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchFiles = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fileService.listFiles();
      setFiles(data);
    } catch (err: any) {
      const errorMessage = getApiErrorMessage(err, 'Failed to fetch files');
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return { files, loading, error, fetchFiles };
};
