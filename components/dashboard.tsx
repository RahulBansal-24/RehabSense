'use client';

import { motion } from 'framer-motion';
import { Dumbbell, TrendingUp, Activity, ArrowRight } from 'lucide-react';
import { GlassCard } from './glass-card';
import { PrimaryButton } from './primary-button';
import { StatCard } from './stat-card';
import { Logo } from './logo';

interface DashboardProps {
  onStartSession: (exercise: string) => void;
}

const exercises = [
  { id: 'squat', name: 'Squats', icon: '🦵', reps: '12-15' },
  { id: 'arm-raise', name: 'Arm Raises', icon: '💪', reps: '10-12' },
  { id: 'shoulder', name: 'Shoulder Rotation', icon: '⚡', reps: '8-10' },
];

export default function Dashboard({ onStartSession }: DashboardProps) {
  const handleSelectExercise = (exerciseId: string) => {
    onStartSession(exerciseId);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen flex flex-col p-4 sm:p-6 lg:p-8"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-12">
        <Logo size="md" showText />
        <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
          <Activity className="w-4 h-4 text-green-600" />
          Active
        </div>
      </div>

      {/* Hero Section */}
      <div className="mb-12">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-3">
            Welcome Back
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl">
            Select your rehabilitation exercise to begin your session with AI-powered form guidance and real-time feedback.
          </p>
        </motion.div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <StatCard
            label="Total Sessions"
            value={24}
            unit="sessions"
            icon={<Activity className="w-5 h-5" />}
            trend="up"
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <StatCard
            label="Average Accuracy"
            value={92}
            unit="%"
            icon={<TrendingUp className="w-5 h-5" />}
            trend="up"
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <StatCard
            label="Total Reps"
            value={428}
            unit="reps"
            icon={<Dumbbell className="w-5 h-5" />}
            trend="up"
          />
        </motion.div>
      </div>

      {/* Exercise Selection */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-foreground mb-6">
          Select Exercise
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {exercises.map((exercise, index) => (
            <motion.div
              key={exercise.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6 + index * 0.1, duration: 0.4 }}
            >
              <GlassCard
                className="cursor-pointer h-full group"
                onClick={() => handleSelectExercise(exercise.id)}
              >
                <div className="flex flex-col items-center gap-4">
                  <div className="text-5xl group-hover:scale-110 transition-transform duration-300">
                    {exercise.icon}
                  </div>
                  <div className="text-center">
                    <h3 className="font-semibold text-foreground mb-1">
                      {exercise.name}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {exercise.reps} reps
                    </p>
                  </div>
                  <PrimaryButton
                    className="w-full mt-4 text-sm py-2"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSelectExercise(exercise.id);
                    }}
                  >
                    Start
                    <ArrowRight className="w-4 h-4" />
                  </PrimaryButton>
                </div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Info Banner */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9, duration: 0.5 }}
        className="mt-auto"
      >
        <GlassCard className="bg-gradient-to-r from-emerald-50/50 to-teal-50/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center text-white flex-shrink-0">
              ✓
            </div>
            <p className="text-sm text-foreground">
              <span className="font-semibold">Tip:</span> Maintain good posture throughout your exercise. The AI will guide you with real-time corrections.
            </p>
          </div>
        </GlassCard>
      </motion.div>
    </motion.div>
  );
}
