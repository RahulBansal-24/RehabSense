"""
Angle Calculator Service - Joint Angle Calculations

This module provides functions to calculate joint angles from landmark coordinates.
Includes helper functions for common exercises (squat, arm raise, shoulder rotation).
"""

from typing import Optional, Dict, Tuple
from utils.helpers import calculate_angle_3d, calculate_angle


class AngleCalculator:
    """
    Service for calculating joint angles from pose landmarks.
    
    Provides methods to calculate angles for different joints and exercises.
    """
    
    @staticmethod
    def calculate_knee_angle(
        hip: Dict,
        knee: Dict,
        ankle: Dict
    ) -> Optional[float]:
        """
        Calculate knee angle (angle at knee joint).
        
        Args:
            hip: Hip landmark with x, y, z coordinates
            knee: Knee landmark with x, y, z coordinates
            ankle: Ankle landmark with x, y, z coordinates
        
        Returns:
            Knee angle in degrees, or None if calculation fails
        """
        try:
            return calculate_angle_3d(
                (hip['x'], hip['y'], hip['z']),
                (knee['x'], knee['y'], knee['z']),
                (ankle['x'], ankle['y'], ankle['z'])
            )
        except Exception:
            return None
    
    @staticmethod
    def calculate_hip_angle(
        shoulder: Dict,
        hip: Dict,
        knee: Dict
    ) -> Optional[float]:
        """
        Calculate hip angle (angle at hip joint).
        
        Args:
            shoulder: Shoulder landmark with x, y, z coordinates
            hip: Hip landmark with x, y, z coordinates
            knee: Knee landmark with x, y, z coordinates
        
        Returns:
            Hip angle in degrees, or None if calculation fails
        """
        try:
            return calculate_angle_3d(
                (shoulder['x'], shoulder['y'], shoulder['z']),
                (hip['x'], hip['y'], hip['z']),
                (knee['x'], knee['y'], knee['z'])
            )
        except Exception:
            return None
    
    @staticmethod
    def calculate_elbow_angle(
        shoulder: Dict,
        elbow: Dict,
        wrist: Dict
    ) -> Optional[float]:
        """
        Calculate elbow angle (angle at elbow joint).
        
        Args:
            shoulder: Shoulder landmark with x, y, z coordinates
            elbow: Elbow landmark with x, y, z coordinates
            wrist: Wrist landmark with x, y, z coordinates
        
        Returns:
            Elbow angle in degrees, or None if calculation fails
        """
        try:
            return calculate_angle_3d(
                (shoulder['x'], shoulder['y'], shoulder['z']),
                (elbow['x'], elbow['y'], elbow['z']),
                (wrist['x'], wrist['y'], wrist['z'])
            )
        except Exception:
            return None
    
    @staticmethod
    def calculate_shoulder_angle(
        elbow: Dict,
        shoulder: Dict,
        hip: Dict
    ) -> Optional[float]:
        """
        Calculate shoulder angle (angle at shoulder joint).
        
        Args:
            elbow: Elbow landmark with x, y, z coordinates
            shoulder: Shoulder landmark with x, y, z coordinates
            hip: Hip landmark with x, y, z coordinates
        
        Returns:
            Shoulder angle in degrees, or None if calculation fails
        """
        try:
            return calculate_angle_3d(
                (elbow['x'], elbow['y'], elbow['z']),
                (shoulder['x'], shoulder['y'], shoulder['z']),
                (hip['x'], hip['y'], hip['z'])
            )
        except Exception:
            return None
    
    @staticmethod
    def get_squat_angles(key_points: Dict) -> Dict[str, Optional[float]]:
        """
        Calculate all relevant angles for squat exercise.
        
        Args:
            key_points: Dictionary of key body points
        
        Returns:
            Dictionary with left and right knee and hip angles
        """
        angles = {
            'left_knee': None,
            'right_knee': None,
            'left_hip': None,
            'right_hip': None
        }
        
        # Left leg angles
        if all(k in key_points for k in ['left_hip', 'left_knee', 'left_ankle']):
            angles['left_knee'] = AngleCalculator.calculate_knee_angle(
                key_points['left_hip'],
                key_points['left_knee'],
                key_points['left_ankle']
            )
        
        if all(k in key_points for k in ['left_shoulder', 'left_hip', 'left_knee']):
            angles['left_hip'] = AngleCalculator.calculate_hip_angle(
                key_points['left_shoulder'],
                key_points['left_hip'],
                key_points['left_knee']
            )
        
        # Right leg angles
        if all(k in key_points for k in ['right_hip', 'right_knee', 'right_ankle']):
            angles['right_knee'] = AngleCalculator.calculate_knee_angle(
                key_points['right_hip'],
                key_points['right_knee'],
                key_points['right_ankle']
            )
        
        if all(k in key_points for k in ['right_shoulder', 'right_hip', 'right_knee']):
            angles['right_hip'] = AngleCalculator.calculate_hip_angle(
                key_points['right_shoulder'],
                key_points['right_hip'],
                key_points['right_knee']
            )
        
        return angles
    
    @staticmethod
    def get_arm_raise_angles(key_points: Dict) -> Dict[str, Optional[float]]:
        """
        Calculate all relevant angles for arm raise exercise.
        
        Args:
            key_points: Dictionary of key body points
        
        Returns:
            Dictionary with left and right shoulder and elbow angles
        """
        angles = {
            'left_shoulder': None,
            'right_shoulder': None,
            'left_elbow': None,
            'right_elbow': None
        }
        
        # Left arm angles
        if all(k in key_points for k in ['left_elbow', 'left_shoulder', 'left_hip']):
            angles['left_shoulder'] = AngleCalculator.calculate_shoulder_angle(
                key_points['left_elbow'],
                key_points['left_shoulder'],
                key_points['left_hip']
            )
        
        if all(k in key_points for k in ['left_shoulder', 'left_elbow', 'left_wrist']):
            angles['left_elbow'] = AngleCalculator.calculate_elbow_angle(
                key_points['left_shoulder'],
                key_points['left_elbow'],
                key_points['left_wrist']
            )
        
        # Right arm angles
        if all(k in key_points for k in ['right_elbow', 'right_shoulder', 'right_hip']):
            angles['right_shoulder'] = AngleCalculator.calculate_shoulder_angle(
                key_points['right_elbow'],
                key_points['right_shoulder'],
                key_points['right_hip']
            )
        
        if all(k in key_points for k in ['right_shoulder', 'right_elbow', 'right_wrist']):
            angles['right_elbow'] = AngleCalculator.calculate_elbow_angle(
                key_points['right_shoulder'],
                key_points['right_elbow'],
                key_points['right_wrist']
            )
        
        return angles
    
    @staticmethod
    def get_shoulder_rotation_angles(key_points: Dict) -> Dict[str, Optional[float]]:
        """
        Calculate all relevant angles for shoulder rotation exercise.
        
        Args:
            key_points: Dictionary of key body points
        
        Returns:
            Dictionary with shoulder rotation angles
        """
        angles = {
            'left_shoulder': None,
            'right_shoulder': None
        }
        
        # Calculate shoulder angles relative to body
        if all(k in key_points for k in ['left_elbow', 'left_shoulder', 'left_hip']):
            angles['left_shoulder'] = AngleCalculator.calculate_shoulder_angle(
                key_points['left_elbow'],
                key_points['left_shoulder'],
                key_points['left_hip']
            )
        
        if all(k in key_points for k in ['right_elbow', 'right_shoulder', 'right_hip']):
            angles['right_shoulder'] = AngleCalculator.calculate_shoulder_angle(
                key_points['right_elbow'],
                key_points['right_shoulder'],
                key_points['right_hip']
            )
        
        return angles
    
    @staticmethod
    def get_exercise_angles(exercise: str, key_points: Dict) -> Dict[str, Optional[float]]:
        """
        Get angles for a specific exercise type.
        
        Args:
            exercise: Exercise type ('squat', 'arm-raise', 'shoulder')
            key_points: Dictionary of key body points
        
        Returns:
            Dictionary with relevant angles for the exercise
        """
        if exercise == 'squat':
            return AngleCalculator.get_squat_angles(key_points)
        elif exercise == 'arm-raise':
            return AngleCalculator.get_arm_raise_angles(key_points)
        elif exercise == 'shoulder':
            return AngleCalculator.get_shoulder_rotation_angles(key_points)
        else:
            return {}
