#!/usr/bin/env python3
"""
Gesture Detection for Air Tic Tac Toe.

This module contains the functionality for detecting hand gestures.
"""

import cv2
import numpy as np
import mediapipe as mp
import time

class GestureDetector:
    """Detects and processes hand gestures for game interaction."""
    
    def __init__(self):
        """Initialize the gesture detector."""
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # X drawing detection parameters
        self.min_drawing_points = 5
        self.drawing_threshold = 0.4
        
        # Trajectory for drawing
        self.trajectory_buffer = []
        self.max_trajectory_length = 50
        
        # Hover detection parameters
        self.hover_cell = None
        self.hover_start_time = 0
        self.hover_threshold = 1.0  # seconds to hover before selecting
        self.is_hovering = False
    
    def process_frame(self, frame):
        """
        Process a frame to detect hands.
        
        Args:
            frame (numpy.ndarray): The frame to process
            
        Returns:
            mediapipe.solutions.hands.Hands: The hand detection results
        """
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process hand landmarks
        results = self.hands.process(rgb_frame)
        
        return results
    
    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on the frame.
        
        Args:
            frame (numpy.ndarray): The frame to draw on
            hand_landmarks: The hand landmarks to draw
            
        Returns:
            numpy.ndarray: The frame with landmarks drawn
        """
        self.mp_drawing.draw_landmarks(
            frame, 
            hand_landmarks, 
            self.mp_hands.HAND_CONNECTIONS)
        
        return frame
    
    def get_finger_position(self, hand_landmarks, frame_shape):
        """
        Get the position of the index finger tip.
        
        Args:
            hand_landmarks: The hand landmarks
            frame_shape (tuple): The shape of the frame (height, width, channels)
            
        Returns:
            tuple: (x, y) coordinates of the index finger tip
        """
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        h, w = frame_shape[:2]
        return int(index_tip.x * w), int(index_tip.y * h)
    
    def is_index_finger_extended(self, hand_landmarks):
        """
        Check if the index finger is extended.
        
        Args:
            hand_landmarks: The hand landmarks
            
        Returns:
            bool: True if the index finger is extended, False otherwise
        """
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        
        return index_tip.y < middle_mcp.y
    
    def update_trajectory(self, point):
        """
        Update the trajectory buffer with a new point.
        
        Args:
            point (tuple): The (x, y) coordinates to add
            
        Returns:
            list: The updated trajectory buffer
        """
        self.trajectory_buffer.append(point)
        if len(self.trajectory_buffer) > self.max_trajectory_length:
            self.trajectory_buffer.pop(0)
        
        return self.trajectory_buffer
    
    def clear_trajectory(self):
        """Clear the trajectory buffer."""
        self.trajectory_buffer = []
    
    def draw_trajectory(self, frame):
        """
        Draw the trajectory on the frame.
        
        Args:
            frame (numpy.ndarray): The frame to draw on
            
        Returns:
            numpy.ndarray: The frame with the trajectory drawn
        """
        if len(self.trajectory_buffer) > 1:
            for i in range(1, len(self.trajectory_buffer)):
                cv2.line(frame, 
                        self.trajectory_buffer[i-1], 
                        self.trajectory_buffer[i], 
                        (0, 165, 255), 2)
        
        return frame
    
    def detect_x_gesture(self):
        """
        Detect if the current trajectory resembles an X shape.
        
        Returns:
            bool: True if an X gesture is detected, False otherwise
        """
        points = self.trajectory_buffer
        
        if len(points) < self.min_drawing_points:
            return False
        
        # Create a simplified representation of the drawing
        points = np.array(points)
        
        # Normalize points to 0-1 range
        min_x, min_y = np.min(points, axis=0)
        max_x, max_y = np.max(points, axis=0)
        
        # Avoid division by zero
        width = max(max_x - min_x, 1)
        height = max(max_y - min_y, 1)
        
        # First, check if the drawing spans a significant area
        # Reduced minimum size requirement
        if width < 15 or height < 15:
            return False
            
        # Simplified X detection: 
        # 1. Check if the drawing covers a reasonable area
        # 2. Check if there are enough direction changes
        
        # Calculate the direction changes
        directions = []
        for i in range(1, len(points)):
            dx = points[i][0] - points[i-1][0]
            dy = points[i][1] - points[i-1][1]
            
            # Classify the direction (4 directions is simpler than 8)
            if abs(dx) > abs(dy):
                # Horizontal movement
                direction = 0 if dx > 0 else 1
            else:
                # Vertical movement
                direction = 2 if dy > 0 else 3
            directions.append(direction)
        
        # Count direction changes
        direction_changes = sum(1 for i in range(1, len(directions)) if directions[i] != directions[i-1])
        
        # An X should have some direction changes
        if direction_changes < 2:
            return False
        
        # More lenient detection - if we have a reasonable sized drawing with some direction changes
        return True
    
    def draw_gesture_feedback(self, frame, position, is_detected):
        """
        Draw visual feedback for gesture detection.
        
        Args:
            frame (numpy.ndarray): The frame to draw on
            position (tuple): The (x, y) position to draw at
            is_detected (bool): Whether a gesture was detected
            
        Returns:
            numpy.ndarray: The frame with feedback drawn
        """
        if is_detected:
            x, y = position
            # Draw a green circle around the cursor to indicate X gesture detected
            cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
            cv2.putText(frame, "X Gesture Detected!", (x - 70, y - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame
    
    def check_hover(self, current_cell):
        """
        Check if the finger is hovering over a cell.
        
        Args:
            current_cell: The current cell (row, col) or None
            
        Returns:
            bool: True if hovering long enough to select, False otherwise
        """
        current_time = time.time()
        
        # If not over any cell, reset hover state
        if current_cell is None:
            self.hover_cell = None
            self.hover_start_time = 0
            self.is_hovering = False
            return False
        
        # If moved to a different cell, reset hover timer
        if self.hover_cell != current_cell:
            self.hover_cell = current_cell
            self.hover_start_time = current_time
            self.is_hovering = True
            return False
        
        # If still in the same cell, check if hover time exceeds threshold
        if self.is_hovering and (current_time - self.hover_start_time) >= self.hover_threshold:
            # Reset hover state after selection
            self.is_hovering = False
            self.hover_start_time = 0
            return True
            
        return False
    
    def draw_hover_feedback(self, frame, cell, game):
        """
        Draw visual feedback for hover detection.
        
        Args:
            frame (numpy.ndarray): The frame to draw on
            cell (tuple): The (row, col) cell being hovered over
            game: The game instance for board coordinates
            
        Returns:
            numpy.ndarray: The frame with hover feedback drawn
        """
        if not self.is_hovering or cell is None or game is None:
            return frame
            
        row, col = cell
        cell_center_x = game.board_offset_x + col * game.cell_size + game.cell_size // 2
        cell_center_y = game.board_offset_y + row * game.cell_size + game.cell_size // 2
        
        # Calculate hover progress (0.0 to 1.0)
        current_time = time.time()
        hover_progress = min(1.0, (current_time - self.hover_start_time) / self.hover_threshold)
        
        # Draw progress circle
        radius = int(game.cell_size * 0.4 * hover_progress)
        thickness = 2
        color = (0, 165, 255)  # Orange
        
        cv2.circle(frame, (cell_center_x, cell_center_y), radius, color, thickness)
        
        # Add text indicator if hovering is significant
        if hover_progress > 0.5:
            cv2.putText(frame, f"{int(hover_progress * 100)}%", 
                      (cell_center_x - 20, cell_center_y - radius - 10),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return frame
    
    def close(self):
        """Release resources."""
        self.hands.close() 