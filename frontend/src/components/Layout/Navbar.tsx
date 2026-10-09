import React, { useState } from 'react';
import { Menu, X, LogOut } from 'lucide-react';
import { useAppDispatch } from '../../hooks';
import { toggleSidebar } from '../../store/slices/uiSlice';

export const Navbar: React.FC = () => {
  const dispatch = useAppDispatch();
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  return (
    <nav className="bg-navy text-white shadow-lg">
      <div className="px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => dispatch(toggleSidebar())}
              className="hidden lg:block hover:bg-blue rounded-lg p-2 transition-colors"
            >
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-2xl font-bold">Weekly Report Agent</h1>
          </div>

          <div className="hidden md:flex items-center gap-4">
            <span className="text-sm text-gray-200">Welcome, User</span>
            <button className="hover:bg-blue rounded-lg p-2 transition-colors">
              <LogOut className="w-5 h-5" />
            </button>
          </div>

          <button
            onClick={() => setShowMobileMenu(!showMobileMenu)}
            className="md:hidden hover:bg-blue rounded-lg p-2 transition-colors"
          >
            {showMobileMenu ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>
    </nav>
  );
};
