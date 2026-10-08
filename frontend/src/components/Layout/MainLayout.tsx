import React from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { Toaster } from 'react-hot-toast';

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-white">
      <Navbar />
      <div className="flex flex-1 min-h-0 overflow-hidden">
        <Sidebar />
        <main className="flex-1 min-w-0 min-h-0 overflow-auto">
          <div className="container mx-auto h-full p-3 sm:p-4 lg:p-6">
            {children}
          </div>
        </main>
      </div>
      <Toaster />
    </div>
  );
};
