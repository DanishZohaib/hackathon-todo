import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  elevation?: "low" | "medium" | "high";
  variant?: "default" | "outlined";
}

const Card: React.FC<CardProps> = ({
  children,
  className = "",
  elevation = "medium",
  variant = "default",
}) => {
  const elevationClasses = {
    low: "shadow-[var(--shadow-low)]",
    medium: "shadow-[var(--shadow-medium)]",
    high: "shadow-[var(--shadow-high)]",
  };

  const variantClasses = {
    default: "glass-effect border border-[var(--bg-glass-border)]",
    outlined: "glass-effect border border-[var(--neon-cyan)]",
  };

  const classes = `
    rounded-lg p-4
    ${elevationClasses[elevation]}
    ${variantClasses[variant]}
    ${className}
  `;

  return (
    <div className={classes}>
      {children}
    </div>
  );
};

export default Card;