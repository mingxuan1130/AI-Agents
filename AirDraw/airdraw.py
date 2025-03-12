import cv2
import numpy as np
import time
import math
from hand_tracking import HandTracker
from drawing_utils import DrawingCanvas
from ui_manager import UIManager

def main():
    """
    Main function to run the AirDraw application.
    """
    # Start capturing video
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera. Please check your camera connection.")
        return
    
    # Get actual frame dimensions
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture video frame. Please check your camera.")
        cap.release()
        return
    
    # Get frame dimensions
    frame_height, frame_width = frame.shape[:2]
    
    # Initialize components
    hand_tracker = HandTracker()
    canvas = DrawingCanvas(frame_width, frame_height)
    ui_manager = UIManager(frame_width, frame_height)
    
    # Print instructions
    ui_manager.print_instructions()
    
    # Create named window and set mouse callback
    cv2.namedWindow("AirDraw")
    
    # Create a custom mouse callback function that passes the canvas to the UI manager
    def mouse_callback(event, x, y, flags, param):
        ui_manager.handle_mouse_event(event, x, y, flags, param, canvas)
    
    cv2.setMouseCallback("AirDraw", mouse_callback)
    
    # Variables for tracking drawing state
    last_drawing_time = time.time()
    
    # Main loop
    try:
        while cap.isOpened() and not ui_manager.exit_program:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame. Camera may have been disconnected.")
                break
            
            frame = cv2.flip(frame, 1)  # Flip frame horizontally
            
            # Process hand landmarks
            results = hand_tracker.process_frame(frame)
            
            # Create a copy of the frame for UI
            ui_frame = frame.copy()
            
            # Add UI elements
            ui_frame = ui_manager.display_ui(
                ui_frame, 
                canvas.current_color_idx, 
                canvas.drawing_mode, 
                canvas.line_mode, 
                canvas.brush_thickness, 
                canvas.special_effect,
                canvas.colors
            )
            
            # Process hand landmarks if detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get index finger tip coordinates
                    index_finger_tip = hand_tracker.get_landmark_position(
                        hand_landmarks, 
                        frame_width, 
                        frame_height, 
                        hand_tracker.mp_hands.HandLandmark.INDEX_FINGER_TIP
                    )
                    
                    # Get middle finger tip for gesture recognition
                    middle_finger_tip = hand_tracker.get_landmark_position(
                        hand_landmarks, 
                        frame_width, 
                        frame_height, 
                        hand_tracker.mp_hands.HandLandmark.MIDDLE_FINGER_TIP
                    )
                    
                    # Calculate distance between index and middle finger tips
                    finger_distance = math.sqrt(
                        (index_finger_tip[0] - middle_finger_tip[0])**2 + 
                        (index_finger_tip[1] - middle_finger_tip[1])**2
                    )
                    
                    # Draw a circle at the index finger tip
                    cv2.circle(ui_frame, index_finger_tip, 10, canvas.current_color, -1)
                    
                    # Check if fingers are close (pinch gesture) - use this to toggle drawing on/off
                    is_drawing = finger_distance > 50  # Only draw when fingers are apart
                    
                    # Draw on canvas
                    current_time = time.time()
                    canvas.prev_point = canvas.draw_point(
                        index_finger_tip[0], 
                        index_finger_tip[1], 
                        is_drawing, 
                        current_time
                    )
                    
                    if is_drawing:
                        last_drawing_time = current_time
                    elif current_time - last_drawing_time > 0.5:
                        # Reset previous point if not drawing for a while
                        canvas.prev_point = None
                    
                    # Draw landmarks
                    hand_tracker.draw_landmarks(ui_frame, hand_landmarks)
            
            # Redraw points if needed
            canvas.redraw_points()
            
            # Combine frame and canvas
            output = ui_manager.combine_frame_and_canvas(ui_frame, canvas.get_canvas())
            
            # Show window
            cv2.imshow("AirDraw", output)
            
            # Check for key presses - only keep ESC for emergency exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key for emergency exit
                print("Emergency exit triggered")
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        print("Releasing resources...")
        hand_tracker.close()
        cap.release()
        cv2.destroyAllWindows()
        print("Program ended successfully.")

if __name__ == "__main__":
    main() 