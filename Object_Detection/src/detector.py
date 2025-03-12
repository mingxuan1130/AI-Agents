"""
Object Detector Module

This module provides the core functionality for real-time object detection
using OpenAI's GPT-4o Vision API.
"""

import cv2
import numpy as np
import base64
import time
import os
import threading
import queue
import json
from openai import OpenAI

# Default configuration
DEFAULT_MODEL = "gpt-4o"  # Using GPT-4o for vision capabilities
DEFAULT_DETECTION_INTERVAL = 2.0  # Seconds between API calls to avoid rate limiting
DEFAULT_CONFIDENCE_THRESHOLD = 0.6  # Minimum confidence score to display a detection

# Colors for different object categories (in BGR format)
COLORS = {
    "person": (0, 255, 0),      # Green
    "animal": (0, 165, 255),    # Orange
    "vehicle": (0, 0, 255),     # Red
    "food": (255, 0, 0),        # Blue
    "electronic": (255, 0, 255), # Purple
    "furniture": (128, 0, 128),  # Purple
    "default": (255, 255, 255)   # White
}

class ObjectDetector:
    """
    Real-time object detector using OpenAI's GPT-4o Vision API.
    
    This class handles the detection of objects in video frames by sending
    images to the OpenAI API and processing the responses.
    """
    
    def __init__(self, api_key, model=DEFAULT_MODEL, 
                 detection_interval=DEFAULT_DETECTION_INTERVAL,
                 confidence_threshold=DEFAULT_CONFIDENCE_THRESHOLD):
        """
        Initialize the object detector.
        
        Args:
            api_key (str): OpenAI API key
            model (str): OpenAI model to use
            detection_interval (float): Seconds between API calls
            confidence_threshold (float): Minimum confidence score for detections
        """
        print(f"Initializing ObjectDetector with model: {model}")
        
        # Initialize OpenAI client
        self.setup_openai_client(api_key)
        
        # Store configuration
        self.model = model
        self.detection_interval = detection_interval
        self.confidence_threshold = confidence_threshold
        
        # Initialize state variables
        self.detections = []
        self.last_detection_time = 0
        self.frame_queue = queue.Queue(maxsize=1)
        self.result_queue = queue.Queue()
        self.is_running = True
        self.lock = threading.Lock()
        self.auto_detect = True  # Flag to control automatic detection
        
        # Start detection thread
        self.detection_thread = threading.Thread(target=self.detection_worker)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        print("Detection thread started")
    
    def setup_openai_client(self, api_key):
        """
        Set up the OpenAI client with the provided API key.
        
        Args:
            api_key (str): OpenAI API key
        """
        # Check API key format, if it's sk-proj format, try special handling
        if api_key.startswith("sk-"):
            print("Setting up OpenAI client...")
            # Ensure environment variable is set
            os.environ["OPENAI_API_KEY"] = api_key
            
            try:
                # Try to initialize client using environment variable
                self.client = OpenAI()
                print("Using environment variable to initialize OpenAI client")
            except Exception as e:
                print(f"Failed to initialize OpenAI client using environment variable: {e}")
                # Fall back to direct API key
                self.client = OpenAI(api_key=api_key)
                print("Falling back to direct API key")
        else:
            print("Invalid API key format")
            raise ValueError("Invalid API key format. API key should start with 'sk-'")
    
    def get_color(self, category):
        """
        Get color for a given object category.
        
        Args:
            category (str): Object category name
            
        Returns:
            tuple: BGR color tuple
        """
        # Find the most appropriate category or use default
        for key in COLORS:
            if key.lower() in category.lower():
                return COLORS[key]
        return COLORS["default"]
    
    def detection_worker(self):
        """
        Background thread to process frames and make API calls.
        """
        while self.is_running:
            try:
                # Only check timing if auto-detect is on
                if self.auto_detect and time.time() - self.last_detection_time < self.detection_interval:
                    time.sleep(0.1)  # Sleep to avoid busy waiting
                    continue
                
                try:
                    frame = self.frame_queue.get(block=False)
                except queue.Empty:
                    time.sleep(0.1)
                    continue
                
                # Encode image for OpenAI API
                _, buffer = cv2.imencode('.jpg', frame)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                
                # Make API call
                try:
                    print("Sending API request...")
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are an object detection system. Identify all visible objects in the image with their bounding box coordinates. Return a JSON array with objects, their confidence scores, and bounding boxes [x1,y1,x2,y2] as proportions of image (0-1)."},
                            {"role": "user", "content": [
                                {"type": "text", "text": "Detect all objects in this image with bounding boxes. Return a JSON array with format [{\"label\": \"object name\", \"confidence\": 0.95, \"bbox\": [x1, y1, x2, y2]}]"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ]
                    )
                    
                    # Parse the response
                    result_text = response.choices[0].message.content.strip()
                    print(f"API response received successfully, length: {len(result_text)} characters")
                    
                    # Extract JSON from response
                    detections = self.extract_json_from_response(result_text)
                    
                    # Filter out low confidence detections
                    valid_detections = [d for d in detections if d.get('confidence', 0) >= self.confidence_threshold]
                    
                    # Update detections with timestamp
                    with self.lock:
                        self.detections = valid_detections
                        self.last_detection_time = time.time()
                        self.result_queue.put(valid_detections)
                        
                    print(f"Detected {len(valid_detections)} objects")
                    
                except Exception as e:
                    print(f"API call error: {e}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Error details: {str(e)}")
                    time.sleep(1)  # Wait before retrying
                
            except Exception as e:
                print(f"Detection thread error: {e}")
                time.sleep(0.1)
    
    def extract_json_from_response(self, result_text):
        """
        Extract JSON data from the API response text.
        
        Args:
            result_text (str): API response text
            
        Returns:
            list: List of detection objects
        """
        try:
            # Try to directly parse the entire response
            detections = json.loads(result_text)
        except json.JSONDecodeError:
            print("Direct JSON parsing failed, attempting to extract JSON portion...")
            # If direct parsing fails, try to extract JSON part
            try:
                if "```json" in result_text:
                    json_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    json_text = result_text.split("```")[1].split("```")[0].strip()
                else:
                    # Try to find JSON array start and end
                    start_idx = result_text.find('[')
                    end_idx = result_text.rfind(']') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        json_text = result_text[start_idx:end_idx]
                    else:
                        # If no JSON array found, try to find JSON object
                        start_idx = result_text.find('{')
                        end_idx = result_text.rfind('}') + 1
                        if start_idx >= 0 and end_idx > start_idx:
                            json_text = result_text[start_idx:end_idx]
                        else:
                            # If no objects detected in response, create empty list
                            print("No JSON data found in response, possibly no objects detected")
                            return []
            
                print(f"Extracted JSON text: {json_text[:100]}...")
                detections = json.loads(json_text)
            except Exception as e:
                print(f"JSON parsing failed: {e}")
                # If all parsing attempts fail, return empty list
                return []
        
        # Ensure detections is a list
        if not isinstance(detections, list):
            if isinstance(detections, dict) and 'objects' in detections:
                detections = detections['objects']
            else:
                print(f"Warning: Detected result is not list format: {type(detections)}")
                detections = []
        
        # Ensure each detection has necessary fields
        valid_detections = []
        for d in detections:
            if isinstance(d, dict) and 'label' in d and 'bbox' in d:
                # Add default confidence if missing
                if 'confidence' not in d:
                    d['confidence'] = 0.9
                
                # Ensure bounding box is correct format [x1, y1, x2, y2]
                if len(d['bbox']) == 4:
                    valid_detections.append(d)
                else:
                    print(f"Warning: Skipping invalid bounding box format: {d['bbox']}")
        
        return valid_detections
    
    def detect_objects(self, frame):
        """
        Queue a frame for processing if ready for a new detection.
        
        Args:
            frame (numpy.ndarray): Video frame to process
        """
        # If the queue is not full and it's time for a new detection
        if not self.frame_queue.full() and time.time() - self.last_detection_time >= self.detection_interval:
            try:
                # Resize frame to reduce API cost and processing time
                height, width = frame.shape[:2]
                max_dim = 800
                if max(height, width) > max_dim:
                    scale = max_dim / max(height, width)
                    frame = cv2.resize(frame, (int(width * scale), int(height * scale)))
                
                self.frame_queue.put(frame.copy(), block=False)
            except queue.Full:
                pass  # Queue is full, skip this frame
    
    def draw_detections(self, frame):
        """
        Draw bounding boxes and labels on the frame.
        
        Args:
            frame (numpy.ndarray): Video frame to draw on
            
        Returns:
            numpy.ndarray: Frame with detections drawn
        """
        height, width = frame.shape[:2]
        
        with self.lock:
            # Display number of detected objects
            num_detections = len(self.detections)
            cv2.putText(frame, f"Detected objects: {num_detections}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw each detection
            for detection in self.detections:
                try:
                    # Get bounding box coordinates
                    bbox = detection.get('bbox', [0, 0, 0, 0])
                    if len(bbox) != 4:
                        print(f"Warning: Skipping invalid bounding box format: {bbox}")
                        continue
                        
                    x1, y1, x2, y2 = bbox
                    
                    # Ensure coordinates are in valid range
                    if not (0 <= x1 <= 1 and 0 <= y1 <= 1 and 0 <= x2 <= 1 and 0 <= y2 <= 1):
                        # If coordinates are not proportions, try to convert them
                        if max(x1, y1, x2, y2) > 1:
                            x1, y1 = x1 / width, y1 / height
                            x2, y2 = x2 / width, y2 / height
                    
                    # Convert to pixel coordinates
                    x1, y1 = int(x1 * width), int(y1 * height)
                    x2, y2 = int(x2 * width), int(y2 * height)
                    
                    # Ensure coordinates are valid
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(width, x2), min(height, y2)
                    
                    # Skip if bounding box is too small
                    if x2 - x1 < 10 or y2 - y1 < 10:
                        continue
                    
                    # Get label and confidence
                    label = detection.get('label', 'unknown')
                    confidence = detection.get('confidence', 0)
                    
                    # Determine color based on object category
                    color = self.get_color(label)
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Prepare label text
                    text = f"{label} ({confidence:.2f})"
                    
                    # Calculate text size and position
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    thickness = 2
                    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                    
                    # Draw text background
                    cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
                    
                    # Draw text
                    cv2.putText(frame, text, (x1, y1 - 5), font, font_scale, (0, 0, 0), thickness)
                except Exception as e:
                    print(f"Error drawing detection result: {e}")
                    continue
        
        # Draw last detection timestamp
        time_since_last = time.time() - self.last_detection_time
        ready_for_new = time_since_last >= self.detection_interval
        
        # Display countdown to next detection
        if not ready_for_new:
            time_remaining = self.detection_interval - time_since_last
            status_text = f"Next detection in: {time_remaining:.1f}s"
            status_color = (0, 165, 255)  # Orange
        else:
            status_text = "Ready for new detection"
            status_color = (0, 255, 0)  # Green
            
        # Draw timestamp and status
        cv2.putText(frame, f"Last detection: {time.strftime('%H:%M:%S', time.localtime(self.last_detection_time))}", 
                   (10, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, status_text, 
                   (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        return frame
    
    def stop(self):
        """
        Stop the detection thread.
        """
        self.is_running = False
        if self.detection_thread.is_alive():
            self.detection_thread.join(timeout=1.0) 