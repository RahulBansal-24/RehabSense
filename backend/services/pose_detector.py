"""
Pose Detection Service - MediaPipe Holistic Integration

This module handles pose detection using MediaPipe Holistic model.
It extracts key body landmarks and returns normalized coordinates.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, List, Tuple
import base64


class PoseDetector:
    """
    Pose detection service using MediaPipe Holistic model.
    
    This class handles initialization of MediaPipe models and provides
    methods to detect poses from image frames.
    """
    
    def __init__(self):
        """Initialize MediaPipe Holistic model for pose detection."""
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        )
    
    def decode_frame(self, frame_data: str) -> Optional[np.ndarray]:
        """
        Decode base64 encoded frame data to OpenCV image format.
        
        Args:
            frame_data: Base64 encoded image string
        
        Returns:
            Decoded image as numpy array, or None if decoding fails
        """
        try:
            # Remove data URL prefix if present
            if ',' in frame_data:
                frame_data = frame_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(frame_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            return image
        except Exception as e:
            print(f"Error decoding frame: {e}")
            return None
    
    def detect_pose(self, image: np.ndarray) -> Optional[Dict]:
        """
        Detect pose landmarks from an image frame.
        
        Args:
            image: Input image as numpy array (BGR format)
        
        Returns:
            Dictionary containing detected landmarks, or None if detection fails
        """
        if image is None:
            return None
        
        try:
            # Convert BGR to RGB (MediaPipe requires RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            
            # Process the image
            results = self.holistic.process(image_rgb)
            
            # Extract landmarks
            landmarks = {
                'pose': None,
                'left_hand': None,
                'right_hand': None,
                'face': None
            }
            
            # Extract pose landmarks
            if results.pose_landmarks:
                landmarks['pose'] = self._extract_landmarks(results.pose_landmarks)
            
            # Extract hand landmarks
            if results.left_hand_landmarks:
                landmarks['left_hand'] = self._extract_landmarks(results.left_hand_landmarks)
            
            if results.right_hand_landmarks:
                landmarks['right_hand'] = self._extract_landmarks(results.right_hand_landmarks)
            
            # Extract face landmarks (optional, for more detailed analysis)
            if results.face_landmarks:
                landmarks['face'] = self._extract_landmarks(results.face_landmarks)
            
            return landmarks
            
        except Exception as e:
            print(f"Error detecting pose: {e}")
            return None
    
    def _extract_landmarks(self, mp_landmarks) -> List[Dict]:
        """
        Extract landmark coordinates from MediaPipe landmarks.
        
        Args:
            mp_landmarks: MediaPipe landmark object
        
        Returns:
            List of dictionaries with x, y, z, visibility for each landmark
        """
        landmarks = []
        if mp_landmarks:
            for landmark in mp_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z if hasattr(landmark, 'z') else 0.0,
                    'visibility': landmark.visibility if hasattr(landmark, 'visibility') else 1.0
                })
        return landmarks
    
    def get_key_points(self, landmarks: Dict) -> Optional[Dict]:
        """
        Extract key body points for exercise analysis.
        
        Args:
            landmarks: Dictionary containing pose landmarks
        
        Returns:
            Dictionary with key body points, or None if pose landmarks not available
        """
        if not landmarks or not landmarks.get('pose'):
            return None
        
        pose_landmarks = landmarks['pose']
        
        # MediaPipe Pose landmark indices
        # Key points for exercise analysis
        key_points = {
            # Upper body
            'left_shoulder': pose_landmarks[11] if len(pose_landmarks) > 11 else None,
            'right_shoulder': pose_landmarks[12] if len(pose_landmarks) > 12 else None,
            'left_elbow': pose_landmarks[13] if len(pose_landmarks) > 13 else None,
            'right_elbow': pose_landmarks[14] if len(pose_landmarks) > 14 else None,
            'left_wrist': pose_landmarks[15] if len(pose_landmarks) > 15 else None,
            'right_wrist': pose_landmarks[16] if len(pose_landmarks) > 16 else None,
            
            # Lower body
            'left_hip': pose_landmarks[23] if len(pose_landmarks) > 23 else None,
            'right_hip': pose_landmarks[24] if len(pose_landmarks) > 24 else None,
            'left_knee': pose_landmarks[25] if len(pose_landmarks) > 25 else None,
            'right_knee': pose_landmarks[26] if len(pose_landmarks) > 26 else None,
            'left_ankle': pose_landmarks[27] if len(pose_landmarks) > 27 else None,
            'right_ankle': pose_landmarks[28] if len(pose_landmarks) > 28 else None,
            
            # Core
            'nose': pose_landmarks[0] if len(pose_landmarks) > 0 else None,
        }
        
        # Filter out None values
        key_points = {k: v for k, v in key_points.items() if v is not None}
        
        return key_points
    
    def cleanup(self):
        """Clean up MediaPipe resources."""
        if hasattr(self, 'holistic'):
            self.holistic.close()


# Global instance (singleton pattern)
_pose_detector_instance: Optional[PoseDetector] = None


def get_pose_detector() -> PoseDetector:
    """
    Get or create the global pose detector instance.
    
    Returns:
        PoseDetector instance
    """
    global _pose_detector_instance
    if _pose_detector_instance is None:
        _pose_detector_instance = PoseDetector()
    return _pose_detector_instance
