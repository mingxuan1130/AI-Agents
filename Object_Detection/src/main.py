"""
Real-time Object Detection System

This script provides a real-time object detection system using OpenAI's GPT-4o
Vision API and a camera (including iPhone camera support).

Usage:
1. Basic usage: python main.py
2. Specify camera: python main.py --camera 1
3. Specify API key: python main.py --api-key "your-api-key"
4. Debug mode: python main.py --debug
5. Manual detection mode: python main.py --manual

Controls:
- ESC: Exit program
- Space: Manually trigger detection
- a: Toggle automatic detection mode
"""

import cv2
import argparse
import sys
import time
import queue
import os

# Import local modules
from detector import ObjectDetector
from camera_utils import open_camera, suggest_camera_connection
from api_utils import validate_api_key, get_api_key

def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Real-time Object Detection using GPT-4 Vision')
    parser.add_argument('--camera', type=int, default=0, help='Camera index')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--api-key', type=str, help='OpenAI API key')
    parser.add_argument('--manual', action='store_true', help='Manual detection mode')
    parser.add_argument('--url', type=str, help='IP camera URL (e.g., http://192.168.1.100:8080/video)')
    return parser.parse_args()

def print_debug_info():
    """
    Print debug information about the system.
    """
    print(f"Python version: {sys.version}")
    print(f"OpenCV version: {cv2.__version__}")
    try:
        import openai
        print(f"OpenAI package version: {openai.__version__}")
    except:
        print("Unable to import openai package or get version")

def print_controls(auto_detect):
    """
    Print control information.
    
    Args:
        auto_detect (bool): Current auto detection status
    """
    print("\nObject Detector Controls:")
    print("-------------------------")
    print("Press 'ESC' to exit")
    print("Press 'SPACE' to manually trigger detection")
    print("Press 'a' to toggle automatic detection mode")
    auto_mode_string = "ON" if auto_detect else "OFF"
    print(f"Auto detection current status: {auto_mode_string}")

def main():
    """
    Main function for the object detection system.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Enable debug mode if requested
    if args.debug:
        print("Debug mode enabled")
        print_debug_info()
    
    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: OpenAI API key not provided.")
        print("Please provide an API key using the --api-key parameter or set the OPENAI_API_KEY environment variable.")
        return
    
    # Validate API key
    is_valid, message = validate_api_key(api_key)
    if not is_valid:
        print(f"Error: {message}")
        print("Please provide a valid OpenAI API key.")
        return
    
    # Open camera
    cap, success = open_camera(args.camera, args.url)
    if not success:
        return
    
    # Initialize object detector
    print("Initializing object detector...")
    detector = ObjectDetector(api_key)
    
    # Set initial auto detection mode based on args
    if args.manual:
        detector.auto_detect = False
        print("Starting in manual detection mode")
    
    # Print controls
    print_controls(detector.auto_detect)
    
    try:
        while True:
            # Read frame from camera
            ret, frame = cap.read()
            if not ret:
                print("Error reading from camera")
                break
            
            # Flip for mirror image (useful for selfie cameras)
            # Comment this line if using rear camera or if you don't want mirroring
            frame = cv2.flip(frame, 1)
            
            # Queue frame for object detection
            detector.detect_objects(frame)
            
            # Draw detections on frame
            output_frame = detector.draw_detections(frame.copy())
            
            # Display instructions and status
            cv2.putText(output_frame, "ESC: Exit | Space: Detect | a: Auto", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            auto_status = "ON" if detector.auto_detect else "OFF"
            cv2.putText(output_frame, f"Auto Detection: {auto_status}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show the resulting frame
            cv2.imshow('Object Detector', output_frame)
            
            # Check for key presses
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                print("Exit request")
                break
            elif key == 32:  # SPACE key - manually trigger detection
                print("Manually triggering detection")
                # Force queue a frame for detection regardless of timing
                try:
                    detector.frame_queue.put(frame.copy(), block=False)
                except queue.Full:
                    # If queue is full, clear it and try again
                    try:
                        detector.frame_queue.get(block=False)
                        detector.frame_queue.put(frame.copy(), block=False)
                    except:
                        pass
            elif key == ord('a'):  # Toggle automatic detection
                detector.auto_detect = not detector.auto_detect
                auto_mode = "Enabled" if detector.auto_detect else "Disabled"
                print(f"Automatic detection {auto_mode}")
    
    except KeyboardInterrupt:
        print("User interrupted")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        print("Releasing resources...")
        detector.stop()
        cap.release()
        cv2.destroyAllWindows()
        print("Program ended successfully")

if __name__ == "__main__":
    main() 