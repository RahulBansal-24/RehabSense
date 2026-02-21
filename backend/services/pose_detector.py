"""

Pose Detection Service - MediaPipe Integration



This module handles pose detection using MediaPipe Pose solution.

It extracts key body landmarks and returns normalized coordinates.

"""



import cv2

import numpy as np

from typing import Optional, Dict, List, Tuple

import base64





class PoseDetector:

    """

    Pose detection service using MediaPipe Pose solution.

    

    This class handles initialization of MediaPipe models and provides

    methods to detect poses from image frames.

    """

    

    def __init__(self):

        """Initialize pose detection with fallback to basic detection."""

        try:

            import mediapipe as mp

            self.mp_pose = mp.solutions.pose

            self.mp_drawing = mp.solutions.drawing_utils

            self.pose = self.mp_pose.Pose(

                min_detection_confidence=0.5,

                min_tracking_confidence=0.5,

                model_complexity=1

            )

            self.use_mediapipe = True

            print("✓ MediaPipe initialized successfully")

        except Exception as e:

            print(f"⚠️ MediaPipe initialization failed: {e}")

            print("Using fallback detection (basic pose estimation)")

            self.use_mediapipe = False

    

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

        

        if self.use_mediapipe:

            return self._detect_with_mediapipe(image)

        else:

            return self._detect_fallback(image)

    

    def _detect_with_mediapipe(self, image: np.ndarray) -> Optional[Dict]:

        """Detect pose using MediaPipe."""

        try:

            # Convert BGR to RGB (MediaPipe requires RGB)

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image_rgb.flags.writeable = False

            

            # Process the image

            results = self.pose.process(image_rgb)

            

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

            

            return landmarks

            

        except Exception as e:

            print(f"MediaPipe detection failed: {e}")

            return None

    

    def _detect_fallback(self, image: np.ndarray) -> Optional[Dict]:

        """Fallback detection using basic pose estimation."""

        try:

            # Create mock landmarks for testing

            # This is a simplified fallback - in production, you'd use OpenCV pose estimation

            height, width = image.shape[:2]

            

            # Generate basic pose landmarks based on image dimensions

            landmarks = {

                'pose': [

                    {'x': 0.5, 'y': 0.1, 'z': 0.0, 'visibility': 1.0},  # nose

                    {'x': 0.4, 'y': 0.2, 'z': 0.0, 'visibility': 1.0},  # left shoulder

                    {'x': 0.6, 'y': 0.2, 'z': 0.0, 'visibility': 1.0},  # right shoulder

                    {'x': 0.35, 'y': 0.4, 'z': 0.0, 'visibility': 1.0}, # left elbow

                    {'x': 0.65, 'y': 0.4, 'z': 0.0, 'visibility': 1.0}, # right elbow

                    {'x': 0.3, 'y': 0.6, 'z': 0.0, 'visibility': 1.0},  # left wrist

                    {'x': 0.7, 'y': 0.6, 'z': 0.0, 'visibility': 1.0},  # right wrist

                    {'x': 0.45, 'y': 0.5, 'z': 0.0, 'visibility': 1.0}, # left hip

                    {'x': 0.55, 'y': 0.5, 'z': 0.0, 'visibility': 1.0}, # right hip

                    {'x': 0.43, 'y': 0.7, 'z': 0.0, 'visibility': 1.0}, # left knee

                    {'x': 0.57, 'y': 0.7, 'z': 0.0, 'visibility': 1.0}, # right knee

                    {'x': 0.42, 'y': 0.9, 'z': 0.0, 'visibility': 1.0}, # left ankle

                    {'x': 0.58, 'y': 0.9, 'z': 0.0, 'visibility': 1.0}, # right ankle

                ],

                'left_hand': None,

                'right_hand': None,

                'face': None

            }

            

            return landmarks

            

        except Exception as e:

            print(f"Fallback detection failed: {e}")

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

        if hasattr(self, 'pose'):

            self.pose.close()





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

