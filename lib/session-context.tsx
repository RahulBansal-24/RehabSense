'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface SessionContextType {
  selectedExercise: string;
  setSelectedExercise: (exercise: string) => void;
  totalReps: number;
  setTotalReps: (reps: number) => void;
  correctReps: number;
  setCorrectReps: (reps: number) => void;
  incorrectReps: number;
  setIncorrectReps: (reps: number) => void;
  postureAccuracy: number;
  setPostureAccuracy: (accuracy: number) => void;
  misalignmentsCount: number;
  setMisalignmentsCount: (count: number) => void;
  incorrectFormAlerts: number;
  setIncorrectFormAlerts: (count: number) => void;
  sessionDuration: number;
  setSessionDuration: (duration: number) => void;
  averageJointDeviation: number;
  setAverageJointDeviation: (deviation: number) => void;
  performanceRating: string;
  setPerformanceRating: (rating: string) => void;
  resetSession: () => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export const SessionProvider = ({ children }: { children: ReactNode }) => {
  const [selectedExercise, setSelectedExercise] = useState<string>('squat');
  const [totalReps, setTotalReps] = useState<number>(0);
  const [correctReps, setCorrectReps] = useState<number>(0);
  const [incorrectReps, setIncorrectReps] = useState<number>(0);
  const [postureAccuracy, setPostureAccuracy] = useState<number>(95);
  const [misalignmentsCount, setMisalignmentsCount] = useState<number>(0);
  const [incorrectFormAlerts, setIncorrectFormAlerts] = useState<number>(0);
  const [sessionDuration, setSessionDuration] = useState<number>(0);
  const [averageJointDeviation, setAverageJointDeviation] = useState<number>(2.5);
  const [performanceRating, setPerformanceRating] = useState<string>('excellent');

  const resetSession = () => {
    setSelectedExercise('squat');
    setTotalReps(0);
    setCorrectReps(0);
    setIncorrectReps(0);
    setPostureAccuracy(95);
    setMisalignmentsCount(0);
    setIncorrectFormAlerts(0);
    setSessionDuration(0);
    setAverageJointDeviation(2.5);
    setPerformanceRating('excellent');
  };

  const value: SessionContextType = {
    selectedExercise,
    setSelectedExercise,
    totalReps,
    setTotalReps,
    correctReps,
    setCorrectReps,
    incorrectReps,
    setIncorrectReps,
    postureAccuracy,
    setPostureAccuracy,
    misalignmentsCount,
    setMisalignmentsCount,
    incorrectFormAlerts,
    setIncorrectFormAlerts,
    sessionDuration,
    setSessionDuration,
    averageJointDeviation,
    setAverageJointDeviation,
    performanceRating,
    setPerformanceRating,
    resetSession,
  };

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
};

export const useSession = () => {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};
