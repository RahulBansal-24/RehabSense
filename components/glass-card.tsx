import React from 'react';
import { cn } from '@/lib/utils';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'sm' | 'lg';
  onClick?: () => void;
}

export function GlassCard({
  children,
  className,
  variant = 'default',
  onClick,
}: GlassCardProps) {
  const variantClasses = {
    default: 'glass-card p-6',
    sm: 'glass-card-sm p-4',
    lg: 'glass-card p-8',
  };

  return (
    <div
      className={cn(variantClasses[variant], className)}
      onClick={onClick}
    >
      {children}
    </div>
  );
}
