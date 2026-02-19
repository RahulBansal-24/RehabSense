'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Square, Clock, Video } from 'lucide-react';
import { GlassCard } from '@/components/glass-card';
import { FeedbackBox } from '@/components/feedback-box';
import { CircularProgress } from '@/components/circular-progress';
import { PrimaryButton } from '@/components/primary-button';
import { SecondaryButton } from '@/components/secondary-button';
import { useSession } from '@/lib/session-context';

const exerciseNames: Record<string, string> = {
  'squat': 'Squats',
  'arm-raise': 'Arm Raises',
  'shoulder': 'Shoulder Rotation',
};

export default function SessionPage() {
  const router = useRouter();
  const {
    selectedExercise,
    setTotalReps,
    setCorrectReps,
    setIncorrectReps,
    setPostureAccuracy,
    setMisalignmentsCount,
    setIncorrectFormAlerts,
    setSessionDuration,
    setAverageJointDeviation,
    setPerformanceRating,
  } = useSession();

  const [reps, setReps] = useState(0);
  const [accuracy, setAccuracy] = useState(95);
  const [isFeedbackCorrect, setIsFeedbackCorrect] = useState(true);
  const [sessionTime, setSessionTime] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setSessionTime((prev) => prev + 1);
      if (Math.random() > 0.72) {
        setReps((prev) => prev + 1);
      }
      if (Math.random() > 0.75) {
        setIsFeedbackCorrect(!isFeedbackCorrect);
      }
      const newAccuracy = Math.floor(Math.random() * 15) + 88;
      setAccuracy(newAccuracy);
    }, 1000);

    return () => clearInterval(timer);
  }, [isFeedbackCorrect]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStopSession = () => {
    const correctCount = Math.floor(reps * 0.85);
    const incorrectCount = reps - correctCount;
    const misalignments = Math.floor(Math.random() * 5) + 2;
    const alerts = Math.floor(Math.random() * 3) + 1;
    const jointDeviation = (Math.random() * 3 + 1.5).toFixed(1);
    const performanceRating =
      accuracy >= 90 ? 'excellent' : accuracy >= 75 ? 'good' : 'needs-improvement';

    setTotalReps(reps);
    setCorrectReps(correctCount);
    setIncorrectReps(incorrectCount);
    setPostureAccuracy(accuracy);
    setMisalignmentsCount(misalignments);
    setIncorrectFormAlerts(alerts);
    setSessionDuration(sessionTime);
    setAverageJointDeviation(parseFloat(jointDeviation as string));
    setPerformanceRating(performanceRating);

    router.push('/summary');
  };

  const exerciseName = exerciseNames[selectedExercise] || 'Exercise';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen p-4 sm:p-6 lg:p-8"
    >
      {/* Header */}
      <div className="mb-8">
        <SecondaryButton
          onClick={() => router.push('/')}
          className="mb-4"
        >
          ← Back
        </SecondaryButton>
        <h1 className="text-3xl font-bold text-foreground">{exerciseName}</h1>
        <p className="text-muted-foreground mt-1">Real-time AI form detection</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Camera Feed - 2/3 width */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          className="lg:col-span-2"
        >
          <GlassCard className="overflow-hidden">
            <div className="aspect-video bg-gradient-to-br from-emerald-50/50 to-teal-50/30 rounded-xl flex items-center justify-center relative group">
              {/* Animated border */}
              <div className="absolute inset-0 rounded-xl border-2 border-transparent bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-padding opacity-0 group-hover:opacity-20 transition-opacity duration-300" />

              <div className="relative z-10 text-center space-y-4">
                <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center shadow-lg shadow-green-500/30">
                  <Video className="w-12 h-12 text-white animate-pulse" />
                </div>
                <div>
                  <p className="font-semibold text-foreground text-lg">
                    Live Camera Feed
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Position yourself in frame for AI analysis
                  </p>
                </div>
              </div>
            </div>
          </GlassCard>

          {/* Feedback indicator */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.4 }}
            className="mt-6"
          >
            <FeedbackBox
              status={isFeedbackCorrect ? 'correct' : 'incorrect'}
              message={
                isFeedbackCorrect
                  ? 'Perfect form! Keep maintaining this posture'
                  : 'Slight adjustment needed - watch your alignment'
              }
            />
          </motion.div>
        </motion.div>

        {/* Right Side Stats Panel - 1/3 width */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          className="space-y-4"
        >
          {/* Reps Counter */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.4 }}
          >
            <GlassCard className="text-center bg-gradient-to-br from-emerald-50/50 to-green-50/30">
              <div className="space-y-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center mx-auto text-white text-xl font-bold shadow-lg shadow-green-500/20">
                  {reps}
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Reps Completed
                  </p>
                  <p className="text-3xl font-bold text-foreground mt-1">
                    {reps}
                  </p>
                </div>
              </div>
            </GlassCard>
          </motion.div>

          {/* Accuracy Circular Progress */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.4 }}
          >
            <GlassCard className="flex flex-col items-center justify-center py-8">
              <CircularProgress
                value={accuracy}
                max={100}
                label="Accuracy"
                size="md"
              />
            </GlassCard>
          </motion.div>

          {/* Session Time */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.4 }}
          >
            <GlassCard className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Clock className="w-4 h-4 text-green-600" />
                <p className="text-sm font-medium text-muted-foreground">
                  Session Time
                </p>
              </div>
              <p className="text-3xl font-bold text-foreground">
                {formatTime(sessionTime)}
              </p>
            </GlassCard>
          </motion.div>

          {/* Stop Session Button */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.4 }}
            className="pt-4"
          >
            <PrimaryButton
              onClick={handleStopSession}
              className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700"
            >
              <Square className="w-4 h-4" />
              Stop Session
            </PrimaryButton>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
}
