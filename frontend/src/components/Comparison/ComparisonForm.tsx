import React, { useState, useEffect } from 'react';
import { useComparison, useFiles } from '../../hooks';
import { Button, Loading } from '../common';
import { CompareRequest, DEFAULT_KEY_COLUMNS } from '../../types';
import { MOVEMENT_THRESHOLD_DEFAULT, MINIMUM_ABSOLUTE_CHANGE_DEFAULT } from '../../utils/constants';
import toast from 'react-hot-toast';

export const ComparisonForm: React.FC<{ onSuccess?: () => void }> = ({ onSuccess }) => {
  const { runComparison, loading } = useComparison();
  const { files, fetchFiles } = useFiles();
  const [formData, setFormData] = useState<CompareRequest>({
    previous_file: '',
    current_file: '',
    key_columns: DEFAULT_KEY_COLUMNS,
    movement_threshold_pct: MOVEMENT_THRESHOLD_DEFAULT,
    minimum_absolute_change: MINIMUM_ABSOLUTE_CHANGE_DEFAULT,
    generate_ai_insights: true,
  });

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.previous_file || !formData.current_file) {
      toast.error('Please select both files');
      return;
    }

    if (formData.previous_file === formData.current_file) {
      toast.error('Please select different files');
      return;
    }

    try {
      await runComparison(formData);
      toast.success('Comparison started successfully!');
      onSuccess?.();
    } catch (error) {
      toast.error('Failed to run comparison');
    }
  };

  if (loading) {
    return <Loading message="Running comparison..." />;
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 space-y-6">
      <h2 className="text-2xl font-bold text-navy">Run Comparison</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Previous File */}
        <div>
          <label className="block text-sm font-semibold text-navy mb-2">
            Previous Week File *
          </label>
          <select
            value={formData.previous_file}
            onChange={(e) => setFormData({ ...formData, previous_file: e.target.value })}
            className="w-full px-4 py-2 border border-mid-grey rounded-lg focus:outline-none focus:ring-2 focus:ring-blue"
          >
            <option value="">Select a file...</option>
            {files.map(file => (
              <option key={file.name} value={file.name}>
                {file.name}
              </option>
            ))}
          </select>
        </div>

        {/* Current File */}
        <div>
          <label className="block text-sm font-semibold text-navy mb-2">
            Current Week File *
          </label>
          <select
            value={formData.current_file}
            onChange={(e) => setFormData({ ...formData, current_file: e.target.value })}
            className="w-full px-4 py-2 border border-mid-grey rounded-lg focus:outline-none focus:ring-2 focus:ring-blue"
          >
            <option value="">Select a file...</option>
            {files.map(file => (
              <option key={file.name} value={file.name}>
                {file.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Key Columns */}
      <div>
        <label className="block text-sm font-semibold text-navy mb-2">
          Key Columns (comma-separated)
        </label>
        <input
          type="text"
          value={formData.key_columns.join(', ')}
          onChange={(e) => setFormData({
            ...formData,
            key_columns: e.target.value.split(',').map(col => col.trim())
          })}
          className="w-full px-4 py-2 border border-mid-grey rounded-lg focus:outline-none focus:ring-2 focus:ring-blue"
          placeholder="e.g., SIREN, Unique Identifier"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Movement Threshold */}
        <div>
          <label className="block text-sm font-semibold text-navy mb-2">
            Movement Threshold (%)
          </label>
          <input
            type="number"
            value={formData.movement_threshold_pct}
            onChange={(e) => setFormData({ ...formData, movement_threshold_pct: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border border-mid-grey rounded-lg focus:outline-none focus:ring-2 focus:ring-blue"
            step="0.1"
            min="0"
          />
        </div>

        {/* Minimum Absolute Change */}
        <div>
          <label className="block text-sm font-semibold text-navy mb-2">
            Minimum Absolute Change
          </label>
          <input
            type="number"
            value={formData.minimum_absolute_change}
            onChange={(e) => setFormData({ ...formData, minimum_absolute_change: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border border-mid-grey rounded-lg focus:outline-none focus:ring-2 focus:ring-blue"
            step="0.01"
            min="0"
          />
        </div>
      </div>

      {/* AI Insights Toggle */}
      <div className="flex items-center gap-3">
        <input
          type="checkbox"
          id="ai_insights"
          checked={formData.generate_ai_insights}
          onChange={(e) => setFormData({ ...formData, generate_ai_insights: e.target.checked })}
          className="w-5 h-5 rounded"
        />
        <label htmlFor="ai_insights" className="text-sm font-medium text-navy">
          Generate AI Insights (using Gemini)
        </label>
      </div>

      <Button type="submit" variant="primary" size="lg" fullWidth isLoading={loading}>
        Run Comparison
      </Button>
    </form>
  );
};
