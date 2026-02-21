"""
WebSocket Router - Real-time Frame Processing

This module provides WebSocket endpoint for real-time webcam frame processing.
It runs pose detection, calculates joint angles, counts reps, checks posture,
and sends feedback back to frontend via WebSocket.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict
import json
import base64
import cv2
import numpy as np

from models.session_models import (
    MetricsUpdate,
    PerformanceRating,
    WebSocketMessage
)
from services.pose_detector import get_pose_detector
from services.angle_calculator import AngleCalculator

router = APIRouter()


@router.get("/ws/health")
async def websocket_health():
    """
    Health check for WebSocket endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy", "websocket": "ready"}
