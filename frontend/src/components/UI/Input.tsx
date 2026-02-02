import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  startAdornment?: React.ReactNode;
  endAdornment?: React.ReactNode;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  startAdornment,
  endAdornment,
  className = "",
  ...props
}) => {
  const hasError = !!error;

  const inputClasses = `
    w-full px-3 py-2 bg-[var(--bg-secondary)]
    text-[var(--text-primary)] border
    ${hasError ? "border-[var(--error-red)]" : "border-[var(--pak-green-primary)]"}
    rounded-md focus:outline-none focus:ring-2
    focus:ring-[var(--pak-green-primary)]
    placeholder-[var(--text-secondary)]
    ${className}
  `;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          {label}
        </label>
      )}
      <div className="relative">
        {startAdornment && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            {startAdornment}
          </div>
        )}
        <input
          {...props}
          className={`${inputClasses} ${startAdornment ? "pl-10" : ""} ${endAdornment ? "pr-10" : ""}`}
        />
        {endAdornment && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {endAdornment}
          </div>
        )}
      </div>
      {helperText && !hasError && (
        <p className="mt-1 text-xs text-[var(--text-secondary)]">{helperText}</p>
      )}
      {error && (
        <p className="mt-1 text-xs text-[var(--error-red)]">{error}</p>
      )}
    </div>
  );
};

export default Input;