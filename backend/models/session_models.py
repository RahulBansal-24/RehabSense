"""
Session Data Models - Pydantic Models for Request/Response Validation

This module defines all Pydantic models for session-related API requests and responses.
These models match the frontend SessionContext structure exactly.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ExerciseType(str, Enum):
    """Supported exercise types"""
    SQUAT = "squat"
    ARM_RAISE = "arm-raise"
    SHOULDER = "shoulder"


class PerformanceRating(str, Enum):
    """Performance rating levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs-improvement"


class SessionStartRequest(BaseModel):
    """
    Request model for starting a new session.
    
    Attributes:
        exercise: Type of exercise to perform
        userId: Optional user identifier
    """
    exercise: ExerciseType = Field(..., description="Type of exercise to perform")
    userId: Optional[str] = Field(None, description="Optional user identifier")


class SessionStartResponse(BaseModel):
    """
    Response model for session start endpoint.
    
    Attributes:
        sessionId: Unique session identifier
        exercise: Type of exercise started
        startedAt: Timestamp when session started
    """
    sessionId: str = Field(..., description="Unique session identifier")
    exercise: str = Field(..., description="Type of exercise")
    startedAt: datetime = Field(..., description="Session start timestamp")


class MetricsUpdate(BaseModel):
    """
    Model for updating session metrics.
    Can be sent via REST API or WebSocket.
    
    Attributes:
        totalReps: Total number of repetitions performed
        correctReps: Number of correctly performed repetitions
        incorrectReps: Number of incorrectly performed repetitions
        postureAccuracy: Posture accuracy percentage (0-100)
        misalignmentsCount: Number of posture misalignments detected
        incorrectFormAlerts: Number of incorrect form alerts
        averageJointDeviation: Average deviation from ideal joint angles (degrees)
    """
    totalReps: int = Field(0, ge=0, description="Total repetitions")
    correctReps: int = Field(0, ge=0, description="Correct repetitions")
    incorrectReps: int = Field(0, ge=0, description="Incorrect repetitions")
    postureAccuracy: float = Field(95.0, ge=0, le=100, description="Posture accuracy percentage")
    misalignmentsCount: int = Field(0, ge=0, description="Number of misalignments")
    incorrectFormAlerts: int = Field(0, ge=0, description="Number of form alerts")
    averageJointDeviation: float = Field(2.5, ge=0, description="Average joint deviation in degrees")


class FrameData(BaseModel):
    """
    Model for incoming frame data from frontend.
    
    Attributes:
        frame: Base64 encoded image data or raw bytes
        timestamp: Frame timestamp
        sessionId: Session identifier
    """
    frame: str = Field(..., description="Base64 encoded image frame")
    timestamp: Optional[float] = Field(None, description="Frame timestamp")
    sessionId: str = Field(..., description="Session identifier")


class FeedbackResponse(BaseModel):
    """
    Response model for metrics update endpoint.
    Contains real-time feedback and session metrics.
    
    Attributes:
        sessionId: Session identifier
        metrics: Current session metrics
        feedback: Real-time feedback message
        performanceRating: Overall performance rating
        alerts: List of current alerts/warnings
    """
    sessionId: str = Field(..., description="Session identifier")
    metrics: MetricsUpdate = Field(..., description="Current session metrics")
    feedback: str = Field(..., description="Real-time feedback message")
    performanceRating: PerformanceRating = Field(..., description="Performance rating")
    alerts: List[str] = Field(default_factory=list, description="Current alerts")


class SessionEndRequest(BaseModel):
    """
    Request model for ending a session.
    
    Attributes:
        sessionId: Session identifier to end
    """
    sessionId: str = Field(..., description="Session identifier")


class SessionSummary(BaseModel):
    """
    Complete session summary returned when session ends.
    Matches frontend SessionContext structure exactly.
    
    Attributes:
        sessionId: Session identifier
        exercise: Type of exercise performed
        totalReps: Total repetitions
        correctReps: Correct repetitions
        incorrectReps: Incorrect repetitions
        postureAccuracy: Final posture accuracy percentage
        misalignmentsCount: Total misalignments detected
        incorrectFormAlerts: Total form alerts
        sessionDuration: Session duration in seconds
        averageJointDeviation: Average joint deviation
        performanceRating: Overall performance rating
        startedAt: Session start timestamp
        endedAt: Session end timestamp
    """
    sessionId: str = Field(..., description="Session identifier")
    exercise: str = Field(..., description="Exercise type")
    totalReps: int = Field(0, ge=0, description="Total repetitions")
    correctReps: int = Field(0, ge=0, description="Correct repetitions")
    incorrectReps: int = Field(0, ge=0, description="Incorrect repetitions")
    postureAccuracy: float = Field(95.0, ge=0, le=100, description="Posture accuracy")
    misalignmentsCount: int = Field(0, ge=0, description="Misalignments count")
    incorrectFormAlerts: int = Field(0, ge=0, description="Form alerts count")
    sessionDuration: int = Field(0, ge=0, description="Duration in seconds")
    averageJointDeviation: float = Field(2.5, ge=0, description="Average joint deviation")
    performanceRating: PerformanceRating = Field(..., description="Performance rating")
    startedAt: datetime = Field(..., description="Start timestamp")
    endedAt: datetime = Field(..., description="End timestamp")


class WebSocketMessage(BaseModel):
    """
    Model for WebSocket messages.
    
    Attributes:
        type: Message type (frame, metrics, feedback)
        data: Message payload
    """
    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
