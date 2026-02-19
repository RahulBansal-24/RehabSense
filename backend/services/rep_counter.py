"""
Repetition Counter Service - Track Exercise Repetitions

This module tracks repetitions based on angle thresholds and handles
correct vs incorrect form detection.
"""

from typing import Dict, Optional, List
from enum import Enum


class RepState(Enum):
    """State machine for repetition tracking"""
    UP = "up"
    DOWN = "down"
    TRANSITION = "transition"


class RepCounter:
    """
    Service for counting exercise repetitions based on joint angles.
    
    Tracks repetitions using a state machine approach with angle thresholds.
    """
    
    def __init__(self, exercise: str):
        """
        Initialize rep counter for a specific exercise.
        
        Args:
            exercise: Exercise type ('squat', 'arm-raise', 'shoulder')
        """
        self.exercise = exercise
        self.total_reps = 0
        self.correct_reps = 0
        self.incorrect_reps = 0
        self.state = RepState.UP
        self.angle_history: List[float] = []
        self.rep_start_angle: Optional[float] = None
        
        # Exercise-specific thresholds
        self.thresholds = self._get_exercise_thresholds(exercise)
    
    def _get_exercise_thresholds(self, exercise: str) -> Dict:
        """
        Get angle thresholds for specific exercise.
        
        Args:
            exercise: Exercise type
        
        Returns:
            Dictionary with threshold values
        """
        thresholds = {
            'squat': {
                'min_angle': 90.0,  # Minimum knee angle for full squat
                'max_angle': 170.0,  # Maximum knee angle for standing
                'correct_range': (85.0, 95.0),  # Correct form range
                'transition_threshold': 120.0  # Angle for state transition
            },
            'arm-raise': {
                'min_angle': 30.0,  # Minimum shoulder angle for raised arm
                'max_angle': 180.0,  # Maximum shoulder angle for lowered arm
                'correct_range': (25.0, 35.0),  # Correct form range
                'transition_threshold': 90.0
            },
            'shoulder': {
                'min_angle': 45.0,  # Minimum rotation angle
                'max_angle': 180.0,  # Maximum rotation angle
                'correct_range': (40.0, 50.0),  # Correct form range
                'transition_threshold': 120.0
            }
        }
        return thresholds.get(exercise, thresholds['squat'])
    
    def update(self, angles: Dict[str, Optional[float]], is_correct_form: bool = True) -> Dict:
        """
        Update rep counter with new angle data.
        
        Args:
            angles: Dictionary of joint angles
            is_correct_form: Whether the current form is correct
        
        Returns:
            Dictionary with updated rep counts and state
        """
        # Get primary angle for this exercise
        primary_angle = self._get_primary_angle(angles)
        
        if primary_angle is None:
            return self._get_status()
        
        # Add to history (keep last 10 values)
        self.angle_history.append(primary_angle)
        if len(self.angle_history) > 10:
            self.angle_history.pop(0)
        
        # State machine logic
        threshold = self.thresholds['transition_threshold']
        
        if self.state == RepState.UP:
            if primary_angle < threshold:
                self.state = RepState.DOWN
                self.rep_start_angle = primary_angle
        elif self.state == RepState.DOWN:
            if primary_angle > threshold:
                # Completed a rep
                self.total_reps += 1
                if is_correct_form:
                    self.correct_reps += 1
                else:
                    self.incorrect_reps += 1
                self.state = RepState.UP
                self.rep_start_angle = None
        
        return self._get_status()
    
    def _get_primary_angle(self, angles: Dict[str, Optional[float]]) -> Optional[float]:
        """
        Get the primary angle for the current exercise.
        
        Args:
            angles: Dictionary of joint angles
        
        Returns:
            Primary angle value, or None if not available
        """
        if self.exercise == 'squat':
            # Use average of left and right knee angles
            knee_angles = []
            if angles.get('left_knee') is not None:
                knee_angles.append(angles['left_knee'])
            if angles.get('right_knee') is not None:
                knee_angles.append(angles['right_knee'])
            return sum(knee_angles) / len(knee_angles) if knee_angles else None
        
        elif self.exercise == 'arm-raise':
            # Use average of left and right shoulder angles
            shoulder_angles = []
            if angles.get('left_shoulder') is not None:
                shoulder_angles.append(angles['left_shoulder'])
            if angles.get('right_shoulder') is not None:
                shoulder_angles.append(angles['right_shoulder'])
            return sum(shoulder_angles) / len(shoulder_angles) if shoulder_angles else None
        
        elif self.exercise == 'shoulder':
            # Use average of left and right shoulder angles
            shoulder_angles = []
            if angles.get('left_shoulder') is not None:
                shoulder_angles.append(angles['left_shoulder'])
            if angles.get('right_shoulder') is not None:
                shoulder_angles.append(angles['right_shoulder'])
            return sum(shoulder_angles) / len(shoulder_angles) if shoulder_angles else None
        
        return None
    
    def _get_status(self) -> Dict:
        """
        Get current rep counter status.
        
        Returns:
            Dictionary with current counts and state
        """
        return {
            'totalReps': self.total_reps,
            'correctReps': self.correct_reps,
            'incorrectReps': self.incorrect_reps,
            'state': self.state.value,
            'currentAngle': self.angle_history[-1] if self.angle_history else None
        }
    
    def reset(self):
        """Reset rep counter to initial state."""
        self.total_reps = 0
        self.correct_reps = 0
        self.incorrect_reps = 0
        self.state = RepState.UP
        self.angle_history = []
        self.rep_start_angle = None
    
    def get_counts(self) -> Dict[str, int]:
        """
        Get current rep counts.
        
        Returns:
            Dictionary with total, correct, and incorrect rep counts
        """
        return {
            'totalReps': self.total_reps,
            'correctReps': self.correct_reps,
            'incorrectReps': self.incorrect_reps
        }
