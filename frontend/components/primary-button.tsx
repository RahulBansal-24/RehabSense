import React from 'react';
import { cn } from '@/lib/utils';

interface PrimaryButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  isLoading?: boolean;
  icon?: React.ReactNode;
}

export function PrimaryButton({
  children,
  className,
  isLoading,
  icon,
  disabled,
  ...props
}: PrimaryButtonProps) {
  return (
    <button
      className={cn(
        'primary-button flex items-center justify-center gap-2',
        isLoading && 'opacity-70 cursor-not-allowed',
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
      disabled={isLoading || disabled}
      {...props}
    >
      {isLoading ? (
        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
      ) : (
        icon
      )}
      {children}
    </button>
  );
}
