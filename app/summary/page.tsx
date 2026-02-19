'use client';

import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { CheckCircle2, ArrowRight, RotateCcw, Activity, Target, AlertCircle, Clock, Gauge } from 'lucide-react';
import { GlassCard } from '@/components/glass-card';
import { PrimaryButton } from '@/components/primary-button';
import { SecondaryButton } from '@/components/secondary-button';
import { useSession } from '@/lib/session-context';

export default function SummaryPage() {
  const router = useRouter();
  const {
    selectedExercise,
    totalReps,
    correctReps,
    incorrectReps,
    postureAccuracy,
    misalignmentsCount,
    incorrectFormAlerts,
    sessionDuration,
    averageJointDeviation,
    performanceRating,
    resetSession,
  } = useSession();

  const exerciseNames: Record<string, string> = {
    'squat': 'Squats',
    'arm-raise': 'Arm Raises',
    'shoulder': 'Shoulder Rotation',
  };

  const exerciseName = exerciseNames[selectedExercise] || 'Exercise';

  const getPerformanceBadge = (rating: string) => {
    switch (rating) {
      case 'excellent':
        return {
          label: 'Excellent',
          color: 'from-emerald-400 to-green-500',
          bg: 'bg-emerald-50/80',
          text: 'text-emerald-700',
        };
      case 'good':
        return {
          label: 'Good',
          color: 'from-green-400 to-teal-500',
          bg: 'bg-green-50/80',
          text: 'text-green-700',
        };
      default:
        return {
          label: 'Needs Improvement',
          color: 'from-blue-400 to-cyan-500',
          bg: 'bg-blue-50/80',
          text: 'text-blue-700',
        };
    }
  };

  const badge = getPerformanceBadge(performanceRating);

  // Calculate consistency score
  const consistencyScore =
    totalReps > 0 ? Math.round((correctReps / totalReps) * 100) : 0;

  // Calculate stability score
  const stabilityScore = Math.max(
    0,
    100 - averageJointDeviation * 15 - misalignmentsCount * 5
  );

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleNewSession = () => {
    resetSession();
    router.push('/');
  };

  const handleBackToDashboard = () => {
    resetSession();
    router.push('/');
  };

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
        className="w-full max-w-5xl"
      >
        {/* Success Icon & Title */}
        <div className="mb-12">
          <motion.div
            className="flex justify-center mb-8"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{
              delay: 0.3,
              type: 'spring',
              stiffness: 100,
            }}
          >
            <div
              className={`w-24 h-24 rounded-full flex items-center justify-center shadow-2xl shadow-green-500/30 bg-gradient-to-br ${badge.color}`}
            >
              <CheckCircle2 className="w-14 h-14 text-white" />
            </div>
          </motion.div>

          <motion.div
            className="text-center space-y-2"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.4 }}
          >
            <h1 className="text-4xl font-bold text-foreground">
              Session Complete!
            </h1>
            <p className="text-lg text-muted-foreground">{exerciseName}</p>
          </motion.div>
        </div>

        {/* Performance Badge */}
        <motion.div
          className="flex justify-center mb-12"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.4 }}
        >
          <div
            className={`px-8 py-4 rounded-full font-semibold text-lg ${badge.bg} ${badge.text} border border-white/40 shadow-lg backdrop-blur-sm`}
          >
            {badge.label}
          </div>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.4 }}
          className="mb-12"
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            {/* Total Reps */}
            <GlassCard className="text-center bg-gradient-to-br from-emerald-50/50 to-green-50/30">
              <div className="flex items-center justify-center mb-3">
                <Activity className="w-5 h-5 text-green-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Total Reps
              </p>
              <p className="text-3xl font-bold text-foreground">{totalReps}</p>
            </GlassCard>

            {/* Correct Reps */}
            <GlassCard className="text-center bg-gradient-to-br from-teal-50/50 to-cyan-50/30">
              <div className="flex items-center justify-center mb-3">
                <CheckCircle2 className="w-5 h-5 text-teal-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Correct Reps
              </p>
              <p className="text-3xl font-bold text-foreground">{correctReps}</p>
            </GlassCard>

            {/* Incorrect Reps */}
            <GlassCard className="text-center bg-gradient-to-br from-orange-50/50 to-amber-50/30">
              <div className="flex items-center justify-center mb-3">
                <AlertCircle className="w-5 h-5 text-orange-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Incorrect Reps
              </p>
              <p className="text-3xl font-bold text-foreground">{incorrectReps}</p>
            </GlassCard>

            {/* Overall Accuracy */}
            <GlassCard className="text-center bg-gradient-to-br from-blue-50/50 to-indigo-50/30">
              <div className="flex items-center justify-center mb-3">
                <Target className="w-5 h-5 text-blue-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Overall Accuracy
              </p>
              <p className="text-3xl font-bold text-foreground">
                {postureAccuracy}%
              </p>
            </GlassCard>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Posture Misalignments */}
            <GlassCard className="text-center bg-gradient-to-br from-red-50/50 to-rose-50/30">
              <div className="flex items-center justify-center mb-3">
                <AlertCircle className="w-5 h-5 text-red-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Posture Misalignments
              </p>
              <p className="text-3xl font-bold text-foreground">
                {misalignmentsCount}
              </p>
            </GlassCard>

            {/* Incorrect Form Alerts */}
            <GlassCard className="text-center bg-gradient-to-br from-yellow-50/50 to-lime-50/30">
              <div className="flex items-center justify-center mb-3">
                <AlertCircle className="w-5 h-5 text-yellow-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Form Alerts
              </p>
              <p className="text-3xl font-bold text-foreground">
                {incorrectFormAlerts}
              </p>
            </GlassCard>

            {/* Session Duration */}
            <GlassCard className="text-center bg-gradient-to-br from-purple-50/50 to-violet-50/30">
              <div className="flex items-center justify-center mb-3">
                <Clock className="w-5 h-5 text-purple-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Session Duration
              </p>
              <p className="text-3xl font-bold text-foreground">
                {formatTime(sessionDuration)}
              </p>
            </GlassCard>

            {/* Avg Joint Deviation */}
            <GlassCard className="text-center bg-gradient-to-br from-pink-50/50 to-fuchsia-50/30">
              <div className="flex items-center justify-center mb-3">
                <Gauge className="w-5 h-5 text-pink-600" />
              </div>
              <p className="text-sm font-medium text-muted-foreground mb-2">
                Avg Joint Deviation
              </p>
              <p className="text-3xl font-bold text-foreground">
                {averageJointDeviation.toFixed(1)}°
              </p>
            </GlassCard>
          </div>
        </motion.div>

        {/* Advanced Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.4 }}
          className="mb-12"
        >
          <h3 className="text-lg font-semibold text-foreground mb-4">
            Advanced Metrics
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Consistency Score */}
            <GlassCard>
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-medium text-muted-foreground">
                  Consistency Score
                </p>
                <span className="text-2xl font-bold text-green-600">
                  {consistencyScore}%
                </span>
              </div>
              <div className="w-full bg-white/30 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${consistencyScore}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Ratio of correct to total repetitions
              </p>
            </GlassCard>

            {/* Stability Score */}
            <GlassCard>
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-medium text-muted-foreground">
                  Stability Score
                </p>
                <span className="text-2xl font-bold text-blue-600">
                  {Math.max(0, Math.round(stabilityScore))}%
                </span>
              </div>
              <div className="w-full bg-white/30 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-blue-400 to-cyan-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${Math.max(0, stabilityScore)}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Joint stability and posture alignment
              </p>
            </GlassCard>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          className="space-y-3 flex flex-col sm:flex-row gap-4"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.4 }}
        >
          <PrimaryButton
            onClick={handleNewSession}
            className="w-full sm:flex-1"
          >
            <RotateCcw className="w-4 h-4" />
            Start New Session
          </PrimaryButton>
          <SecondaryButton
            onClick={handleBackToDashboard}
            className="w-full sm:flex-1"
          >
            <ArrowRight className="w-4 h-4" />
            Back to Dashboard
          </SecondaryButton>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
