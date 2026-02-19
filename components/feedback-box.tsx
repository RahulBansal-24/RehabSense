import React from 'react';
import { CheckCircle2, AlertCircle } from 'lucide-react';

interface FeedbackBoxProps {
  status: 'correct' | 'incorrect' | 'neutral';
  message: string;
  showAnimation?: boolean;
}

export function FeedbackBox({
  status,
  message,
  showAnimation = true,
}: FeedbackBoxProps) {
  const statusConfig = {
    correct: {
      bg: 'bg-green-50',
      border: 'border-green-200/40',
      text: 'text-green-700',
      icon: CheckCircle2,
      shadow: 'shadow-green-500/20',
    },
    incorrect: {
      bg: 'bg-red-50',
      border: 'border-red-200/40',
      text: 'text-red-700',
      icon: AlertCircle,
      shadow: 'shadow-red-500/20',
    },
    neutral: {
      bg: 'bg-blue-50',
      border: 'border-blue-200/40',
      text: 'text-blue-700',
      icon: AlertCircle,
      shadow: 'shadow-blue-500/20',
    },
  };

  const config = statusConfig[status];
  const IconComponent = config.icon;

  return (
    <div
      className={`${config.bg} border ${config.border} rounded-xl p-4 flex items-center gap-3 backdrop-blur-sm shadow-lg ${config.shadow} ${
        showAnimation ? 'animate-pulse' : ''
      }`}
    >
      <IconComponent className={`w-6 h-6 ${config.text} flex-shrink-0`} />
      <p className={`${config.text} font-medium text-sm`}>{message}</p>
    </div>
  );
}
