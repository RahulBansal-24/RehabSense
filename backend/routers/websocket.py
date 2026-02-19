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
from routers.session import sessions, calculate_performance_rating

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time frame processing.
    
    Accepts webcam frames, processes them for pose detection,
    calculates metrics, and sends feedback back to client.
    
    Args:
        websocket: WebSocket connection
        session_id: Session identifier
    """
    await websocket.accept()
    
    # Verify session exists
    if session_id not in sessions:
        await websocket.close(code=1008, reason="Session not found")
        return
    
    session = sessions[session_id]
    exercise = session['exercise']
    rep_counter = session['repCounter']
    posture_analyzer = session['postureAnalyzer']
    pose_detector = get_pose_detector()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get('type', 'frame')
                
                if message_type == 'frame':
                    # Process frame data
                    frame_data = message.get('data', {}).get('frame', '')
                    
                    if not frame_data:
                        continue
                    
                    # Decode frame
                    image = pose_detector.decode_frame(frame_data)
                    
                    if image is None:
                        continue
                    
                    # Detect pose
                    landmarks = pose_detector.detect_pose(image)
                    
                    if landmarks and landmarks.get('pose'):
                        # Get key points
                        key_points = pose_detector.get_key_points(landmarks)
                        
                        if key_points:
                            # Calculate angles for the exercise
                            angles = AngleCalculator.get_exercise_angles(exercise, key_points)
                            
                            # Analyze posture
                            posture_analysis = posture_analyzer.analyze(angles)
                            
                            # Check form correctness
                            is_correct_form = posture_analyzer.check_form_correctness(angles)
                            
                            # Update rep counter
                            rep_status = rep_counter.update(angles, is_correct_form)
                            
                            # Update session metrics
                            session['metrics'].update({
                                'totalReps': rep_status['totalReps'],
                                'correctReps': rep_status['correctReps'],
                                'incorrectReps': rep_status['incorrectReps'],
                                'postureAccuracy': posture_analysis['postureAccuracy'],
                                'misalignmentsCount': posture_analysis['misalignmentsCount'],
                                'incorrectFormAlerts': posture_analysis['incorrectFormAlerts'],
                                'averageJointDeviation': posture_analysis['averageJointDeviation']
                            })
                            
                            # Calculate performance rating
                            performance_rating = calculate_performance_rating(
                                session['metrics']['postureAccuracy'],
                                session['metrics']['correctReps'],
                                session['metrics']['totalReps']
                            )
                            
                            # Prepare response
                            response = {
                                'type': 'feedback',
                                'data': {
                                    'sessionId': session_id,
                                    'metrics': {
                                        'totalReps': session['metrics']['totalReps'],
                                        'correctReps': session['metrics']['correctReps'],
                                        'incorrectReps': session['metrics']['incorrectReps'],
                                        'postureAccuracy': session['metrics']['postureAccuracy'],
                                        'misalignmentsCount': session['metrics']['misalignmentsCount'],
                                        'incorrectFormAlerts': session['metrics']['incorrectFormAlerts'],
                                        'averageJointDeviation': session['metrics']['averageJointDeviation']
                                    },
                                    'performanceRating': performance_rating.value,
                                    'alerts': posture_analysis.get('alerts', []),
                                    'angles': {k: v for k, v in angles.items() if v is not None}
                                }
                            }
                            
                            # Send response back to client
                            await websocket.send_json(response)
                
                elif message_type == 'ping':
                    # Respond to ping with pong
                    await websocket.send_json({'type': 'pong', 'data': {}})
                
                elif message_type == 'close':
                    # Client requested to close connection
                    break
            
            except json.JSONDecodeError:
                # Invalid JSON, skip
                continue
            except Exception as e:
                # Send error response
                error_response = {
                    'type': 'error',
                    'data': {
                        'message': str(e)
                    }
                }
                await websocket.send_json(error_response)
    
    except WebSocketDisconnect:
        # Client disconnected normally
        pass
    except Exception as e:
        # Unexpected error
        print(f"WebSocket error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass


@router.get("/ws/health")
async def websocket_health():
    """
    Health check for WebSocket endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy", "websocket": "ready"}
