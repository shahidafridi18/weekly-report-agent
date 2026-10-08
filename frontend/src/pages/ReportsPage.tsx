import React from 'react';
import { ReportGenerator, ReportHistory } from '../components/Reports';

export const ReportsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-navy mb-2">Reports</h1>
        <p className="text-dark-grey">Generate and manage your comparison reports</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Generator */}
        <div className="lg:col-span-1">
          <ReportGenerator />
        </div>

        {/* History */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-bold text-navy mb-4">Report History</h2>
          <ReportHistory />
        </div>
      </div>
    </div>
  );
};
