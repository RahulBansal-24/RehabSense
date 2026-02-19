import React from 'react';
import { GlassCard } from './glass-card';

interface StatCardProps {
  label: string;
  value: string | number;
  unit?: string;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
}

export function StatCard({
  label,
  value,
  unit,
  icon,
  trend = 'neutral',
}: StatCardProps) {
  const trendColor = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-slate-600',
  };

  return (
    <GlassCard variant="sm" className="text-center">
      <div className="flex flex-col items-center gap-3">
        {icon && (
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center text-white">
            {icon}
          </div>
        )}
        <p className="text-sm font-medium text-muted-foreground">{label}</p>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-foreground">{value}</span>
          {unit && (
            <span className={`text-sm font-medium ${trendColor[trend]}`}>
              {unit}
            </span>
          )}
        </div>
      </div>
    </GlassCard>
  );
}
