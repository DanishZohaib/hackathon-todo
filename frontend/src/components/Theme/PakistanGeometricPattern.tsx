import React from "react";

interface PakistanGeometricPatternProps {
  className?: string;
}

const PakistanGeometricPattern: React.FC<PakistanGeometricPatternProps> = ({ className = '' }) => {
  return (
    <div className={`absolute inset-0 overflow-hidden opacity-5 ${className}`}>
      <svg
        className="absolute inset-0 w-full h-full"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid slice"
      >
        {/* Star pattern - representing the star in Pakistan flag */}
        <defs>
          <pattern
            id="pak-pattern"
            x="0"
            y="0"
            width="20"
            height="20"
            patternUnits="userSpaceOnUse"
          >
            <polygon
              points="10,2 12,7 18,7 13,10 15,15 10,12 5,15 7,10 2,7 8,7"
              fill="var(--pak-green-primary)"
              opacity="0.3"
            />
          </pattern>
        </defs>
        <rect x="0" y="0" width="100" height="100" fill="url(#pak-pattern)" />
      </svg>
    </div>
  );
};

export default PakistanGeometricPattern;