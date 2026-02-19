import React from 'react';
import { cn } from '@/lib/utils';

interface SecondaryButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  icon?: React.ReactNode;
}

export function SecondaryButton({
  children,
  className,
  icon,
  ...props
}: SecondaryButtonProps) {
  return (
    <button
      className={cn(
        'secondary-button flex items-center justify-center gap-2',
        className
      )}
      {...props}
    >
      {icon}
      {children}
    </button>
  );
}
