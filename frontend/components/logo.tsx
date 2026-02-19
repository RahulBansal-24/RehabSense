import React from 'react';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
}

export function Logo({ size = 'md', showText = true }: LogoProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
  };

  const textSize = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
  };

  return (
    <div className="flex items-center gap-3">
      <div className={`${sizeClasses[size]} relative`}>
        <svg
          viewBox="0 0 40 40"
          className="w-full h-full"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Medical cross */}
          <rect
            x="16"
            y="8"
            width="8"
            height="24"
            fill="url(#crossGradient)"
            rx="2"
          />
          <rect
            x="8"
            y="16"
            width="24"
            height="8"
            fill="url(#crossGradient)"
            rx="2"
          />

          {/* Motion wave */}
          <path
            d="M 8 24 Q 12 20 16 24 T 24 24"
            stroke="url(#waveGradient)"
            strokeWidth="2"
            fill="none"
            strokeLinecap="round"
          />
          <path
            d="M 8 28 Q 12 24 16 28 T 24 28"
            stroke="url(#waveGradient)"
            strokeWidth="1.5"
            fill="none"
            strokeLinecap="round"
            opacity="0.6"
          />

          <defs>
            <linearGradient id="crossGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#16A34A" />
              <stop offset="100%" stopColor="#22C55E" />
            </linearGradient>
            <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {showText && (
        <div className="flex flex-col">
          <span className={`font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent ${textSize[size]}`}>
            RehabSense
          </span>
          <span className="text-xs font-medium text-muted-foreground leading-none">
            AI Rehabilitation
          </span>
        </div>
      )}
    </div>
  );
}
