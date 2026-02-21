'use client';

import { useState, useEffect, useRef } from 'react';
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
  const [feedback, setFeedback] = useState('Perfect form! Keep maintaining this posture');
  const [frame, setFrame] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null); // Debug mode
  
  const websocketRef = useRef<WebSocket | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // WebSocket connection
  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_BACKEND_WS || 'ws://localhost:8000/ws/pose';
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log('✅ WebSocket connected');
      setIsConnected(true);
      
      // Send exercise selection
      ws.send(JSON.stringify({
        exercise: selectedExercise
      }));
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("WS DATA:", data); // Step 3: WebSocket data logging
        
        // Handle both test_response and direct feedback messages
        if (data.type === "test_response") {
          const actual = data.received;
          console.log("TEST RESPONSE DATA:", actual);
          
          // Step 4: Fix response field mapping
          const mappedData = {
            reps: Number(actual.reps || 0),
            correct_reps: Number(actual.correct_reps || 0),
            incorrect_reps: Number(actual.incorrect_reps || 0),
            accuracy: Number(actual.accuracy || 0),
            feedback: actual.feedback || "Analyzing...",
            posture_correct: Boolean(actual.posture_correct),
            frame: actual.frame || null
          };
          
          console.log("MAPPED DATA:", mappedData);
          
          // Step 5: Fix NaN values
          setReps(mappedData.reps);
          setCorrectReps(mappedData.correct_reps);
          setIncorrectReps(mappedData.incorrect_reps);
          setAccuracy(mappedData.accuracy);
          setFeedback(mappedData.feedback);
          setIsFeedbackCorrect(mappedData.posture_correct);
          setFrame(mappedData.frame);
          
          // Update session context
          setTotalReps(mappedData.reps);
          setCorrectReps(mappedData.correct_reps);
          setIncorrectReps(mappedData.incorrect_reps);
          setPostureAccuracy(mappedData.accuracy);
          setMisalignmentsCount(Number(actual.misalignments || 0));
          setIncorrectFormAlerts(Number(actual.alerts || 0));
          setAverageJointDeviation(Number(actual.joint_deviation || 0));
          
        } else if (data.type === 'feedback') {
          console.log("FEEDBACK DATA:", data);
          
          // Step 4: Fix response field mapping
          const mappedData = {
            reps: Number(data.reps || 0),
            correct_reps: Number(data.correct_reps || 0),
            incorrect_reps: Number(data.incorrect_reps || 0),
            accuracy: Number(data.accuracy || 0),
            feedback: data.feedback || "Analyzing...",
            posture_correct: Boolean(data.posture_correct),
            frame: data.frame || null
          };
          
          console.log("MAPPED FEEDBACK DATA:", mappedData);
          
          // Step 5: Fix NaN values
          setReps(mappedData.reps);
          setCorrectReps(mappedData.correct_reps);
          setIncorrectReps(mappedData.incorrect_reps);
          setAccuracy(mappedData.accuracy);
          setFeedback(mappedData.feedback);
          setIsFeedbackCorrect(mappedData.posture_correct);
          setFrame(mappedData.frame);
          
          // Update session context
          setTotalReps(mappedData.reps);
          setCorrectReps(mappedData.correct_reps);
          setIncorrectReps(mappedData.incorrect_reps);
          setPostureAccuracy(mappedData.accuracy);
          setMisalignmentsCount(Number(data.misalignments || 0));
          setIncorrectFormAlerts(Number(data.alerts || 0));
          setAverageJointDeviation(Number(data.joint_deviation || 0));
        }
        
        setLastMessage(data); // Debug mode
        
      } catch (error) {
        console.error('❌ Error parsing WebSocket message:', error);
      }
    };
    
    ws.onclose = () => {
      console.log('🔌 WebSocket disconnected');
      setIsConnected(false);
    };
    
    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
      setIsConnected(false);
    };
    
    websocketRef.current = ws;
    
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [selectedExercise, setTotalReps, setCorrectReps, setIncorrectReps, setPostureAccuracy, setMisalignmentsCount, setIncorrectFormAlerts, setAverageJointDeviation]);

  // Camera setup and frame sending
  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: 640, height: 480 } 
        });
        streamRef.current = stream;
        
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        
        // Part 1: Frame throttling - send every 150ms (≈6 FPS)
        const captureAndSendFrame = () => {
          if (videoRef.current && canvasRef.current && websocketRef.current?.readyState === WebSocket.OPEN) {
            const video = videoRef.current;
            const canvas = canvasRef.current;
            const context = canvas.getContext('2d');
            
            if (context && video.readyState === video.HAVE_ENOUGH_DATA) {
              console.log("Step 1: Running detection - capturing frame"); // Step 1 debugging
              
              canvas.width = 640;
              canvas.height = 480;
              context.drawImage(video, 0, 0, canvas.width, canvas.height);
              
              const frameData = canvas.toDataURL('image/jpeg', 0.7); // Lower quality for speed
              
              console.log("Step 3: Sending frame to backend"); // Step 3 debugging
              
              // Send frame to backend
              websocketRef.current.send(JSON.stringify({
                frame: frameData
              }));
            }
          }
        };
        
        // Part 1: Send frames at 6 FPS instead of 15 FPS
        intervalRef.current = setInterval(captureAndSendFrame, 150);
        
      } catch (error) {
        console.error('Error accessing camera:', error);
      }
    };
    
    startCamera();
    
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  // Session timer
  useEffect(() => {
    const timer = setInterval(() => {
      setSessionTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Step 4: Force rerender check
  useEffect(() => {
    console.log("Frame updated:", !!frame);
  }, [frame]);

  // Step 6: Verify React state is actually updating
  useEffect(() => {
    console.log("Stats updated:", { reps, accuracy, feedback, isFeedbackCorrect });
  }, [reps, accuracy, feedback, isFeedbackCorrect]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStopSession = () => {
    // Close WebSocket
    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      websocketRef.current.close();
    }
    
    // Stop camera
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    // Calculate performance rating
    const performanceRating =
      accuracy >= 90 ? 'excellent' : accuracy >= 75 ? 'good' : 'needs-improvement';

    // Save final stats to session context
    setSessionDuration(sessionTime);
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
      {/* Hidden video and canvas for camera processing */}
      <video ref={videoRef} autoPlay playsInline className="hidden" />
      <canvas ref={canvasRef} className="hidden" />

      {/* Header */}
      <div className="mb-8">
        <SecondaryButton
          onClick={() => router.push('/')}
          className="mb-4"
        >
          ← Back
        </SecondaryButton>
        <h1 className="text-3xl font-bold text-foreground">{exerciseName}</h1>
        <p className="text-muted-foreground mt-1">
          Real-time AI form detection {isConnected ? '✅' : '🔄 Connecting...'}
        </p>
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
            <div className="relative w-full h-[480px] bg-black rounded-xl overflow-hidden">
              {frame && (
                <img
                  src={frame}
                  alt="Live Feed"
                  className="w-full h-full object-contain"
                  style={{ transform: "scaleX(-1)" }}
                />
              )}
            </div>
          </GlassCard>

          {/* Step 7: Debug visibility */}
          <div className="mt-4 p-2 bg-black/10 rounded text-sm">
            <div className="text-white">
              {frame ? "✅ FRAME RECEIVED" : "❌ NO FRAME"}
            </div>
            <div className="text-white">
              Reps: {reps} | Accuracy: {accuracy}%
            </div>
            <div className="text-white">
              Connected: {isConnected ? "✅" : "❌"}
            </div>
          </div>

          {/* Feedback indicator */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.4 }}
            className="mt-6"
          >
            <FeedbackBox
              status={isFeedbackCorrect ? 'correct' : 'incorrect'}
              message={feedback}
            />
          </motion.div>

          {/* Debug mode - Phase 7 */}
          {lastMessage && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7, duration: 0.4 }}
              className="mt-4"
            >
              <GlassCard className="p-4">
                <h3 className="text-sm font-semibold text-muted-foreground mb-2">🔍 Debug Mode</h3>
                <pre className="text-xs bg-black/5 p-2 rounded overflow-auto max-h-32">
                  {JSON.stringify(lastMessage, null, 2)}
                </pre>
              </GlassCard>
            </motion.div>
          )}
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
