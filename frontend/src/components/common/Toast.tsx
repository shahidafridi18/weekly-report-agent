import React from 'react';
import { AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';
import toast from 'react-hot-toast';
import { Notification } from '../../store/slices/uiSlice';

const notificationTypeConfig = {
  success: {
    icon: CheckCircle,
    bgColor: 'bg-green-50',
    textColor: 'text-green-800',
    borderColor: 'border-green-200',
  },
  error: {
    icon: AlertCircle,
    bgColor: 'bg-red-50',
    textColor: 'text-red-800',
    borderColor: 'border-red-200',
  },
  info: {
    icon: Info,
    bgColor: 'bg-blue-50',
    textColor: 'text-blue-800',
    borderColor: 'border-blue-200',
  },
  warning: {
    icon: AlertTriangle,
    bgColor: 'bg-yellow-50',
    textColor: 'text-yellow-800',
    borderColor: 'border-yellow-200',
  },
};

interface ToastProps {
  notification: Notification;
}

export const Toast: React.FC<ToastProps> = ({ notification }) => {
  const config = notificationTypeConfig[notification.type];
  const Icon = config.icon;

  return (
    <div
      className={`${config.bgColor} ${config.textColor} border ${config.borderColor} rounded-lg p-4 flex items-center gap-3`}
    >
      <Icon className="w-5 h-5" />
      <span className="text-sm font-medium">{notification.message}</span>
    </div>
  );
};

export const showToast = (message: string, type: 'success' | 'error' | 'info' | 'warning' = 'info') => {
  const config = notificationTypeConfig[type];
  const Icon = config.icon;

  toast.custom(() => (
    <div
      className={`${config.bgColor} ${config.textColor} border ${config.borderColor} rounded-lg p-4 flex items-center gap-3 shadow-lg`}
    >
      <Icon className="w-5 h-5" />
      <span className="text-sm font-medium">{message}</span>
    </div>
  ), {
    duration: 4000,
  });
};
