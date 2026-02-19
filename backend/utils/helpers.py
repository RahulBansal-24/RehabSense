"""
Helper Utilities - Reusable Functions for Vector Math, Thresholds, and Smoothing

This module provides utility functions used across the backend services.
"""

import numpy as np
from typing import List, Tuple, Optional


def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two 2D points.
    
    Args:
        point1: First point as (x, y)
        point2: Second point as (x, y)
    
    Returns:
        Distance between the two points
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_distance_3d(point1: Tuple[float, float, float], point2: Tuple[float, float, float]) -> float:
    """
    Calculate Euclidean distance between two 3D points.
    
    Args:
        point1: First point as (x, y, z)
        point2: Second point as (x, y, z)
    
    Returns:
        Distance between the two points
    """
    return np.sqrt(
        (point1[0] - point2[0])**2 + 
        (point1[1] - point2[1])**2 + 
        (point1[2] - point2[2])**2
    )


def calculate_angle(
    point1: Tuple[float, float], 
    point2: Tuple[float, float], 
    point3: Tuple[float, float]
) -> float:
    """
    Calculate the angle at point2 formed by points point1-point2-point3.
    
    Args:
        point1: First point (x, y)
        point2: Vertex point (x, y)
        point3: Third point (x, y)
    
    Returns:
        Angle in degrees (0-180)
    """
    # Convert to numpy arrays
    a = np.array(point1)
    b = np.array(point2)
    c = np.array(point3)
    
    # Calculate vectors
    ba = a - b
    bc = c - b
    
    # Calculate angle using dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # Clamp to avoid numerical errors
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)


def calculate_angle_3d(
    point1: Tuple[float, float, float], 
    point2: Tuple[float, float, float], 
    point3: Tuple[float, float, float]
) -> float:
    """
    Calculate the angle at point2 formed by points point1-point2-point3 in 3D space.
    
    Args:
        point1: First point (x, y, z)
        point2: Vertex point (x, y, z)
        point3: Third point (x, y, z)
    
    Returns:
        Angle in degrees (0-180)
    """
    # Convert to numpy arrays
    a = np.array(point1)
    b = np.array(point2)
    c = np.array(point3)
    
    # Calculate vectors
    ba = a - b
    bc = c - b
    
    # Calculate angle using dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # Clamp to avoid numerical errors
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)


def smooth_values(values: List[float], window_size: int = 5) -> List[float]:
    """
    Apply moving average smoothing to a list of values.
    
    Args:
        values: List of numeric values to smooth
        window_size: Size of the moving average window
    
    Returns:
        List of smoothed values
    """
    if len(values) < window_size:
        return values
    
    smoothed = []
    for i in range(len(values)):
        start = max(0, i - window_size // 2)
        end = min(len(values), i + window_size // 2 + 1)
        smoothed.append(np.mean(values[start:end]))
    
    return smoothed


def check_threshold(value: float, threshold: float, tolerance: float = 0.0) -> bool:
    """
    Check if a value meets a threshold with optional tolerance.
    
    Args:
        value: Value to check
        threshold: Threshold value
        tolerance: Tolerance range (default: 0)
    
    Returns:
        True if value is within threshold ± tolerance
    """
    return abs(value - threshold) <= tolerance


def check_range(value: float, min_val: float, max_val: float) -> bool:
    """
    Check if a value is within a specified range.
    
    Args:
        value: Value to check
        min_val: Minimum value
        max_val: Maximum value
    
    Returns:
        True if value is within range [min_val, max_val]
    """
    return min_val <= value <= max_val


def normalize_landmark(landmark, image_width: int, image_height: int) -> Tuple[float, float]:
    """
    Normalize landmark coordinates from MediaPipe format to pixel coordinates.
    
    Args:
        landmark: MediaPipe landmark object
        image_width: Width of the image
        image_height: Height of the image
    
    Returns:
        Normalized coordinates as (x, y)
    """
    x = landmark.x * image_width
    y = landmark.y * image_height
    return (x, y)


def calculate_midpoint(
    point1: Tuple[float, float], 
    point2: Tuple[float, float]
) -> Tuple[float, float]:
    """
    Calculate the midpoint between two points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
    
    Returns:
        Midpoint as (x, y)
    """
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)


def calculate_midpoint_3d(
    point1: Tuple[float, float, float], 
    point2: Tuple[float, float, float]
) -> Tuple[float, float, float]:
    """
    Calculate the midpoint between two 3D points.
    
    Args:
        point1: First point (x, y, z)
        point2: Second point (x, y, z)
    
    Returns:
        Midpoint as (x, y, z)
    """
    return (
        (point1[0] + point2[0]) / 2,
        (point1[1] + point2[1]) / 2,
        (point1[2] + point2[2]) / 2
    )


def is_landmark_visible(landmark) -> bool:
    """
    Check if a MediaPipe landmark is visible.
    
    Args:
        landmark: MediaPipe landmark object
    
    Returns:
        True if landmark visibility > 0.5
    """
    return hasattr(landmark, 'visibility') and landmark.visibility > 0.5


def calculate_deviation(actual: float, ideal: float) -> float:
    """
    Calculate deviation from ideal value.
    
    Args:
        actual: Actual value
        ideal: Ideal value
    
    Returns:
        Absolute deviation
    """
    return abs(actual - ideal)


def calculate_percentage_score(actual: float, ideal: float, max_deviation: float) -> float:
    """
    Calculate a percentage score based on deviation from ideal.
    
    Args:
        actual: Actual value
        ideal: Ideal value
        max_deviation: Maximum allowed deviation (100% score threshold)
    
    Returns:
        Score as percentage (0-100)
    """
    deviation = calculate_deviation(actual, ideal)
    if deviation >= max_deviation:
        return 0.0
    return max(0.0, 100.0 * (1.0 - deviation / max_deviation))
