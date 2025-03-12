import mediapipe as mp
import cv2
import os
import logging

# Suppress TensorFlow and MediaPipe warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging
logging.getLogger('mediapipe').setLevel(logging.ERROR)  # Suppress MediaPipe logging

class HandTracker:
    """
    A class for tracking hand movements using MediaPipe.
    Provides functionality to detect and track hand landmarks.
    """
    
    def __init__(self, static_image_mode=False, max_num_hands=1, 
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize the hand tracker with specified parameters.
        
        Args:
            static_image_mode (bool): Whether to treat input as static images
            max_num_hands (int): Maximum number of hands to detect
            min_detection_confidence (float): Minimum confidence for detection
            min_tracking_confidence (float): Minimum confidence for tracking
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize MediaPipe Hands with optimized parameters
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def process_frame(self, frame):
        """
        Process a video frame to detect hand landmarks.
        
        Args:
            frame (numpy.ndarray): Input video frame
            
        Returns:
            results: MediaPipe hand detection results
        """
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and find hands
        results = self.hands.process(rgb_frame)
        return results
    
    def draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on the frame.
        
        Args:
            frame (numpy.ndarray): Frame to draw on
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            numpy.ndarray: Frame with landmarks drawn
        """
        self.mp_drawing.draw_landmarks(
            frame, 
            hand_landmarks, 
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )
        return frame
    
    def get_landmark_position(self, hand_landmarks, frame_width, frame_height, landmark_index):
        """
        Get the position of a specific landmark.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            frame_width (int): Width of the frame
            frame_height (int): Height of the frame
            landmark_index: Index of the landmark to get
            
        Returns:
            tuple: (x, y) coordinates of the landmark
        """
        landmark = hand_landmarks.landmark[landmark_index]
        x, y = int(landmark.x * frame_width), int(landmark.y * frame_height)
        return (x, y)
    
    def close(self):
        """
        Release resources used by the hand tracker.
        """
        self.hands.close() 