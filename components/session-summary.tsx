'use client';

import { motion } from 'framer-motion';
import { CheckCircle2, ArrowRight, RotateCcw } from 'lucide-react';
import { GlassCard } from './glass-card';
import { PrimaryButton } from './primary-button';
import { SecondaryButton } from './secondary-button';

interface SessionSummaryProps {
  sessionData: {
    exercise: string;
    totalReps: number;
    accuracy: number;
  };
  onNewSession: () => void;
  onBackToDashboard: () => void;
}

export default function SessionSummary({
  sessionData,
  onNewSession,
  onBackToDashboard,
}: SessionSummaryProps) {
  const getPerformanceBadge = (accuracy: number) => {
    if (accuracy >= 90) {
      return {
        label: 'Excellent',
        color: 'from-emerald-400 to-green-500',
        bg: 'bg-emerald-50/80',
        text: 'text-emerald-700',
      };
    } else if (accuracy >= 75) {
      return {
        label: 'Good',
        color: 'from-green-400 to-teal-500',
        bg: 'bg-green-50/80',
        text: 'text-green-700',
      };
    } else {
      return {
        label: 'Needs Improvement',
        color: 'from-blue-400 to-cyan-500',
        bg: 'bg-blue-50/80',
        text: 'text-blue-700',
      };
    }
  };

  const badge = getPerformanceBadge(sessionData.accuracy);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen flex items-center justify-center p-4"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.5 }}
        className="w-full max-w-md"
      >
        <GlassCard className="p-8 md:p-12 space-y-8">
          {/* Success Icon */}
          <motion.div
            className="flex justify-center"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{
              delay: 0.3,
              type: 'spring',
              stiffness: 100,
            }}
          >
            <div className={`w-24 h-24 rounded-full flex items-center justify-center shadow-2xl shadow-green-500/30 bg-gradient-to-br ${badge.color}`}>
              <CheckCircle2 className="w-14 h-14 text-white" />
            </div>
          </motion.div>

          {/* Title */}
          <motion.div
            className="text-center space-y-2"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.4 }}
          >
            <h1 className="text-4xl font-bold text-foreground">
              Session Complete!
            </h1>
            <p className="text-lg text-muted-foreground">{sessionData.exercise}</p>
          </motion.div>

          {/* Results Grid */}
          <motion.div
            className="grid grid-cols-2 gap-4"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.4 }}
          >
            <GlassCard variant="sm" className="text-center bg-gradient-to-br from-emerald-50/50 to-green-50/30">
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Total Reps
              </p>
              <p className="text-4xl font-bold text-green-600">
                {sessionData.totalReps}
              </p>
            </GlassCard>
            <GlassCard variant="sm" className="text-center bg-gradient-to-br from-teal-50/50 to-cyan-50/30">
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Accuracy
              </p>
              <p className="text-4xl font-bold text-teal-600">
                {sessionData.accuracy}%
              </p>
            </GlassCard>
          </motion.div>

          {/* Performance Badge */}
          <motion.div
            className="flex justify-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.4 }}
          >
            <div
              className={`px-8 py-4 rounded-full font-semibold text-lg ${badge.bg} ${badge.text} border border-white/40 shadow-lg backdrop-blur-sm`}
            >
              {badge.label}
            </div>
          </motion.div>

          {/* Buttons */}
          <motion.div
            className="space-y-3 pt-4"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.4 }}
          >
            <PrimaryButton onClick={onNewSession} className="w-full">
              <RotateCcw className="w-4 h-4" />
              Start New Session
            </PrimaryButton>
            <SecondaryButton onClick={onBackToDashboard} className="w-full">
              <ArrowRight className="w-4 h-4" />
              Back to Dashboard
            </SecondaryButton>
          </motion.div>
        </GlassCard>
      </motion.div>
    </motion.div>
  );
}
