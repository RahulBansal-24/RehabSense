"""
Session Router - REST API Endpoints for Session Management

This module provides REST endpoints for:
- Starting a session
- Updating session metrics
- Ending a session and getting summary
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict
import uuid
import time

from models.session_models import (
    SessionStartRequest,
    SessionStartResponse,
    MetricsUpdate,
    FeedbackResponse,
    SessionEndRequest,
    SessionSummary,
    PerformanceRating
)
from services.pose_detector import get_pose_detector
from services.angle_calculator import AngleCalculator
from services.rep_counter import RepCounter
from services.posture_analyzer import PostureAnalyzer

router = APIRouter()

# In-memory session storage (use database in production)
sessions: Dict[str, Dict] = {}


def calculate_performance_rating(posture_accuracy: float, correct_reps: int, total_reps: int) -> PerformanceRating:
    """
    Calculate performance rating based on metrics.
    
    Args:
        posture_accuracy: Posture accuracy percentage
        correct_reps: Number of correct repetitions
        total_reps: Total number of repetitions
    
    Returns:
        Performance rating enum value
    """
    if total_reps == 0:
        return PerformanceRating.NEEDS_IMPROVEMENT
    
    correct_ratio = correct_reps / total_reps if total_reps > 0 else 0.0
    
    if posture_accuracy >= 90.0 and correct_ratio >= 0.85:
        return PerformanceRating.EXCELLENT
    elif posture_accuracy >= 75.0 and correct_ratio >= 0.70:
        return PerformanceRating.GOOD
    else:
        return PerformanceRating.NEEDS_IMPROVEMENT


@router.post("/sessions/start", response_model=SessionStartResponse)
async def start_session(request: SessionStartRequest):
    """
    Start a new exercise session.
    
    Args:
        request: Session start request with exercise type
    
    Returns:
        Session start response with sessionId and metadata
    """
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Initialize session services
        rep_counter = RepCounter(request.exercise.value)
        posture_analyzer = PostureAnalyzer(request.exercise.value)
        
        # Store session data
        sessions[session_id] = {
            'sessionId': session_id,
            'exercise': request.exercise.value,
            'startedAt': datetime.now(),
            'repCounter': rep_counter,
            'postureAnalyzer': posture_analyzer,
            'metrics': {
                'totalReps': 0,
                'correctReps': 0,
                'incorrectReps': 0,
                'postureAccuracy': 95.0,
                'misalignmentsCount': 0,
                'incorrectFormAlerts': 0,
                'averageJointDeviation': 2.5
            }
        }
        
        return SessionStartResponse(
            sessionId=session_id,
            exercise=request.exercise.value,
            startedAt=sessions[session_id]['startedAt']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@router.post("/sessions/{session_id}/metrics", response_model=FeedbackResponse)
async def update_metrics(session_id: str, metrics: MetricsUpdate):
    """
    Update session metrics (can be called with or without frame data).
    
    Args:
        session_id: Session identifier
        metrics: Updated metrics data
    
    Returns:
        Feedback response with current metrics and feedback message
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        session = sessions[session_id]
        
        # Update session metrics
        session['metrics'].update(metrics.dict())
        
        # Calculate performance rating
        performance_rating = calculate_performance_rating(
            session['metrics']['postureAccuracy'],
            session['metrics']['correctReps'],
            session['metrics']['totalReps']
        )
        
        # Generate feedback message
        feedback = _generate_feedback(session['metrics'], performance_rating)
        
        # Generate alerts
        alerts = []
        if session['metrics']['misalignmentsCount'] > 0:
            alerts.append(f"Detected {session['metrics']['misalignmentsCount']} posture misalignments")
        if session['metrics']['incorrectFormAlerts'] > 0:
            alerts.append(f"{session['metrics']['incorrectFormAlerts']} incorrect form alerts")
        
        return FeedbackResponse(
            sessionId=session_id,
            metrics=MetricsUpdate(**session['metrics']),
            feedback=feedback,
            performanceRating=performance_rating,
            alerts=alerts
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update metrics: {str(e)}")


@router.post("/sessions/{session_id}/end", response_model=SessionSummary)
async def end_session(session_id: str, request: SessionEndRequest):
    """
    End a session and return final summary.
    
    Args:
        session_id: Session identifier
        request: Session end request
    
    Returns:
        Complete session summary matching frontend SessionContext structure
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        session = sessions[session_id]
        ended_at = datetime.now()
        started_at = session['startedAt']
        
        # Calculate session duration
        duration = int((ended_at - started_at).total_seconds())
        
        # Get final metrics
        metrics = session['metrics']
        
        # Calculate final performance rating
        performance_rating = calculate_performance_rating(
            metrics['postureAccuracy'],
            metrics['correctReps'],
            metrics['totalReps']
        )
        
        # Create session summary
        summary = SessionSummary(
            sessionId=session_id,
            exercise=session['exercise'],
            totalReps=metrics['totalReps'],
            correctReps=metrics['correctReps'],
            incorrectReps=metrics['incorrectReps'],
            postureAccuracy=metrics['postureAccuracy'],
            misalignmentsCount=metrics['misalignmentsCount'],
            incorrectFormAlerts=metrics['incorrectFormAlerts'],
            sessionDuration=duration,
            averageJointDeviation=metrics['averageJointDeviation'],
            performanceRating=performance_rating,
            startedAt=started_at,
            endedAt=ended_at
        )
        
        # Clean up session (optional - keep for debugging)
        # del sessions[session_id]
        
        return summary
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end session: {str(e)}")


def _generate_feedback(metrics: Dict, performance_rating: PerformanceRating) -> str:
    """
    Generate human-readable feedback message based on metrics.
    
    Args:
        metrics: Current session metrics
        performance_rating: Performance rating
    
    Returns:
        Feedback message string
    """
    if metrics['totalReps'] == 0:
        return "Start your exercise! Keep your form correct."
    
    if performance_rating == PerformanceRating.EXCELLENT:
        return f"Excellent form! {metrics['correctReps']}/{metrics['totalReps']} reps were perfect. Keep it up!"
    elif performance_rating == PerformanceRating.GOOD:
        return f"Good work! {metrics['correctReps']}/{metrics['totalReps']} reps were correct. Focus on maintaining form."
    else:
        return f"Keep practicing! {metrics['correctReps']}/{metrics['totalReps']} reps were correct. Focus on your posture."
