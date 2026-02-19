"""
Posture Analyzer Service - Posture Analysis and Scoring

This module compares current pose to ideal posture, detects misalignments,
and generates posture scores (0-100%).
"""

from typing import Dict, Optional, List, Tuple
from services.angle_calculator import AngleCalculator
from utils.helpers import calculate_deviation, calculate_percentage_score


class PostureAnalyzer:
    """
    Service for analyzing posture and detecting misalignments.
    
    Compares current pose to ideal posture and generates scores and alerts.
    """
    
    def __init__(self, exercise: str):
        """
        Initialize posture analyzer for a specific exercise.
        
        Args:
            exercise: Exercise type ('squat', 'arm-raise', 'shoulder')
        """
        self.exercise = exercise
        self.ideal_angles = self._get_ideal_angles(exercise)
        self.misalignments_count = 0
        self.incorrect_form_alerts = 0
        self.joint_deviations: List[float] = []
    
    def _get_ideal_angles(self, exercise: str) -> Dict[str, float]:
        """
        Get ideal angles for specific exercise.
        
        Args:
            exercise: Exercise type
        
        Returns:
            Dictionary with ideal angle values
        """
        ideal = {
            'squat': {
                'left_knee': 90.0,
                'right_knee': 90.0,
                'left_hip': 90.0,
                'right_hip': 90.0
            },
            'arm-raise': {
                'left_shoulder': 30.0,
                'right_shoulder': 30.0,
                'left_elbow': 180.0,
                'right_elbow': 180.0
            },
            'shoulder': {
                'left_shoulder': 45.0,
                'right_shoulder': 45.0
            }
        }
        return ideal.get(exercise, {})
    
    def analyze(self, angles: Dict[str, Optional[float]]) -> Dict:
        """
        Analyze current posture and compare to ideal.
        
        Args:
            angles: Dictionary of current joint angles
        
        Returns:
            Dictionary with analysis results including score, misalignments, and alerts
        """
        deviations = []
        misalignments = []
        alerts = []
        
        # Check each angle against ideal
        for angle_name, current_angle in angles.items():
            if current_angle is None:
                continue
            
            ideal_angle = self.ideal_angles.get(angle_name)
            if ideal_angle is None:
                continue
            
            # Calculate deviation
            deviation = calculate_deviation(current_angle, ideal_angle)
            deviations.append(deviation)
            
            # Check for misalignment (deviation > threshold)
            threshold = self._get_misalignment_threshold(angle_name)
            if deviation > threshold:
                misalignments.append({
                    'joint': angle_name,
                    'deviation': deviation,
                    'ideal': ideal_angle,
                    'actual': current_angle
                })
                self.misalignments_count += 1
            
            # Generate alerts for severe misalignments
            severe_threshold = threshold * 2
            if deviation > severe_threshold:
                alerts.append(f"Severe misalignment in {angle_name}: {deviation:.1f}° deviation")
                self.incorrect_form_alerts += 1
        
        # Calculate average deviation
        avg_deviation = sum(deviations) / len(deviations) if deviations else 0.0
        self.joint_deviations.append(avg_deviation)
        
        # Keep only last 50 deviations
        if len(self.joint_deviations) > 50:
            self.joint_deviations.pop(0)
        
        # Calculate posture accuracy score (0-100)
        # Score decreases as deviation increases
        max_allowed_deviation = 15.0  # Maximum deviation for 0% score
        posture_accuracy = calculate_percentage_score(
            avg_deviation, 
            0.0, 
            max_allowed_deviation
        )
        
        return {
            'postureAccuracy': round(posture_accuracy, 2),
            'averageJointDeviation': round(avg_deviation, 2),
            'misalignments': misalignments,
            'alerts': alerts,
            'misalignmentsCount': len(misalignments),
            'incorrectFormAlerts': len(alerts)
        }
    
    def _get_misalignment_threshold(self, angle_name: str) -> float:
        """
        Get misalignment threshold for a specific joint.
        
        Args:
            angle_name: Name of the joint angle
        
        Returns:
            Threshold value in degrees
        """
        # Default thresholds (can be customized per joint)
        thresholds = {
            'knee': 10.0,
            'hip': 12.0,
            'shoulder': 15.0,
            'elbow': 10.0
        }
        
        # Match joint name to threshold
        for key, threshold in thresholds.items():
            if key in angle_name.lower():
                return threshold
        
        return 12.0  # Default threshold
    
    def check_form_correctness(self, angles: Dict[str, Optional[float]]) -> bool:
        """
        Check if current form is correct.
        
        Args:
            angles: Dictionary of current joint angles
        
        Returns:
            True if form is correct, False otherwise
        """
        analysis = self.analyze(angles)
        
        # Form is correct if:
        # 1. Posture accuracy > 80%
        # 2. No severe misalignments
        # 3. Average deviation < 10 degrees
        return (
            analysis['postureAccuracy'] > 80.0 and
            analysis['misalignmentsCount'] == 0 and
            analysis['averageJointDeviation'] < 10.0
        )
    
    def get_average_deviation(self) -> float:
        """
        Get average joint deviation over recent frames.
        
        Returns:
            Average deviation in degrees
        """
        if not self.joint_deviations:
            return 0.0
        return sum(self.joint_deviations) / len(self.joint_deviations)
    
    def reset(self):
        """Reset analyzer state."""
        self.misalignments_count = 0
        self.incorrect_form_alerts = 0
        self.joint_deviations = []
    
    def get_summary(self) -> Dict:
        """
        Get posture analysis summary.
        
        Returns:
            Dictionary with summary statistics
        """
        return {
            'misalignmentsCount': self.misalignments_count,
            'incorrectFormAlerts': self.incorrect_form_alerts,
            'averageJointDeviation': self.get_average_deviation()
        }
