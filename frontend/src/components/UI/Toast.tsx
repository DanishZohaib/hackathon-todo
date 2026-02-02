import React, { useEffect } from "react";

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'info' | 'warning';
  onClose: () => void;
  duration?: number;
}

const Toast: React.FC<ToastProps> = ({
  message,
  type = 'info',
  onClose,
  duration = 5000
}) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const typeStyles = {
    success: 'bg-[var(--pak-green-primary)] border-[var(--pak-green-primary)]',
    error: 'bg-[var(--error-red)] border-[var(--error-red)]',
    info: 'bg-[var(--bg-secondary)] border-[var(--pak-green-primary)]',
    warning: 'bg-[var(--accent-gold)] border-[var(--accent-gold)] text-[var(--bg-primary)]'
  };

  return (
    <div
      className={`
        fixed bottom-4 right-4 z-50 p-4 rounded-md border
        ${typeStyles[type]}
        transform transition-transform duration-300
        animate-fadeInUp
      `}
    >
      <div className="flex items-center">
        <span className="mr-2">{message}</span>
        <button
          onClick={onClose}
          className="ml-4 text-current hover:opacity-75 focus:outline-none"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Toast;