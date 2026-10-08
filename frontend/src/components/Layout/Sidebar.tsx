import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Home,
  BarChart3,
  FileText,
  MessageSquare,
  Settings,
} from 'lucide-react';
import { useAppSelector } from '../../hooks';
import clsx from 'clsx';

const navItems = [
  { label: 'Dashboard', path: '/', icon: Home },
  { label: 'Comparison', path: '/comparison', icon: BarChart3 },
  { label: 'Reports', path: '/reports', icon: FileText },
  { label: 'Chat', path: '/chat', icon: MessageSquare },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const sidebarOpen = useAppSelector(state => state.ui.sidebarOpen);

  return (
    <aside
      className={clsx(
        'bg-pale-blue border-r border-mid-grey transition-all duration-300',
        sidebarOpen ? 'w-64' : 'w-20',
        'hidden lg:block h-full flex-shrink-0 overflow-y-auto'
      )}
    >
      <div className="p-4 space-y-8">
        <nav className="space-y-2">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={clsx(
                  'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                  isActive
                    ? 'bg-blue text-white'
                    : 'text-dark-grey hover:bg-light-blue'
                )}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && <span className="text-sm font-medium">{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-mid-grey pt-4">
          <button className={clsx(
            'flex items-center gap-3 px-4 py-3 rounded-lg w-full transition-colors',
            'text-dark-grey hover:bg-light-blue'
          )}>
            <Settings className="w-5 h-5" />
            {sidebarOpen && <span className="text-sm font-medium">Settings</span>}
          </button>
        </div>
      </div>
    </aside>
  );
};
