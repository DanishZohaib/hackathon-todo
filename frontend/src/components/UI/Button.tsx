import React from "react";

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  className?: string;
  type?: "button" | "submit" | "reset";
}

const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = "primary",
  size = "md",
  disabled = false,
  className = "",
  type = "button",
}) => {
  // Base classes
  const baseClasses = "inline-flex items-center justify-center rounded-md font-medium transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent hover:scale-[1.02] active:scale-[0.98]";

  // Size variants
  const sizeClasses = {
    sm: "text-xs px-3 py-1.5",
    md: "text-sm px-4 py-2",
    lg: "text-base px-6 py-3",
  };

  // Variant variants
  const variantClasses = {
    primary: "bg-gradient-to-r from-[var(--neon-cyan)] to-[var(--neon-purple)] text-white hover:from-[var(--neon-purple)] hover:to-[var(--neon-cyan)] focus:ring-[var(--neon-cyan)] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-glow",
    secondary: "bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--neon-cyan)] hover:bg-[var(--neon-cyan)] hover:text-white focus:ring-[var(--neon-cyan)] disabled:opacity-50 disabled:cursor-not-allowed",
    outline: "border border-[var(--neon-cyan)] bg-transparent text-[var(--neon-cyan)] hover:bg-[var(--neon-cyan)] hover:text-[var(--bg-primary)] focus:ring-[var(--neon-cyan)] disabled:opacity-50 disabled:cursor-not-allowed",
    ghost: "bg-transparent text-[var(--neon-cyan)] hover:bg-[var(--neon-cyan)] hover:text-[var(--bg-primary)] focus:ring-[var(--neon-cyan)] disabled:opacity-50 disabled:cursor-not-allowed",
  };

  const classes = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;