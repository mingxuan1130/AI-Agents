import cv2

class UIManager:
    """
    A class for managing the user interface of the AirDraw application.
    Handles UI rendering and user interactions with UI elements.
    """
    
    def __init__(self, frame_width, frame_height):
        """
        Initialize the UI manager with specified frame dimensions.
        
        Args:
            frame_width (int): Width of the frame
            frame_height (int): Height of the frame
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.exit_program = False
    
    def display_ui(self, img, color_idx, drawing_mode, line_mode, brush_thickness, special_effect, colors):
        """
        Display UI elements on the frame.
        
        Args:
            img (numpy.ndarray): Frame to draw UI on
            color_idx (int): Index of the current color
            drawing_mode (bool): Current drawing mode
            line_mode (bool): Current line mode
            brush_thickness (int): Current brush thickness
            special_effect (int): Current special effect
            colors (list): List of available colors
            
        Returns:
            numpy.ndarray: Frame with UI elements
        """
        # Display color palette
        for i in range(len(colors)):
            cv2.rectangle(img, (10 + i*30, 10), (30 + i*30, 30), colors[i], -1)
        
        # Highlight selected color
        cv2.rectangle(img, (10 + color_idx * 30, 10), (30 + color_idx * 30, 30), (255, 255, 255), 2)
        
        # Display mode buttons
        draw_mode_text = "Draw" if drawing_mode else "Erase"
        cv2.rectangle(img, (130, 10), (230, 40), (50, 50, 50), -1)
        cv2.putText(img, f"Mode: {draw_mode_text}", (135, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        line_mode_text = "Line" if line_mode else "Dots"
        cv2.rectangle(img, (230, 10), (330, 40), (50, 50, 50), -1)
        cv2.putText(img, f"Style: {line_mode_text}", (235, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        effect_names = ["No Effect", "Rainbow", "Glow"]
        cv2.rectangle(img, (330, 10), (430, 40), (50, 50, 50), -1)
        cv2.putText(img, f"Effect: {effect_names[special_effect]}", (335, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Thickness controls
        cv2.rectangle(img, (self.frame_width - 300, 10), (self.frame_width - 250, 40), (50, 50, 50), -1)
        cv2.putText(img, f"Size: {brush_thickness}", (self.frame_width - 295, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Split the +/- button visually to show it has two functions
        cv2.rectangle(img, (self.frame_width - 250, 10), (self.frame_width - 225, 40), (50, 50, 50), -1)
        cv2.putText(img, "-", (self.frame_width - 240, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        cv2.rectangle(img, (self.frame_width - 225, 10), (self.frame_width - 200, 40), (50, 50, 50), -1)
        cv2.putText(img, "+", (self.frame_width - 220, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Add clickable buttons
        cv2.rectangle(img, (self.frame_width - 200, 10), (self.frame_width - 100, 40), (0, 0, 200), -1)
        cv2.putText(img, "CLEAR", (self.frame_width - 180, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        cv2.rectangle(img, (self.frame_width - 100, 10), (self.frame_width - 20, 40), (200, 0, 0), -1)
        cv2.putText(img, "EXIT", (self.frame_width - 80, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Display instructions
        cv2.putText(img, "Click on buttons to change settings", (10, self.frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return img
    
    def handle_mouse_event(self, event, x, y, flags, param, canvas):
        """
        Handle mouse events for UI interaction.
        
        Args:
            event (int): Mouse event type
            x (int): X-coordinate of the mouse event
            y (int): Y-coordinate of the mouse event
            flags (int): Mouse event flags
            param: Additional parameters
            canvas: Drawing canvas object
            
        Returns:
            bool: Whether the program should exit
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if click is in the exit button area
            if x > self.frame_width - 100 and y < 50:
                self.exit_program = True
            
            # Check if click is in the clear button area
            elif x > self.frame_width - 200 and x < self.frame_width - 100 and y < 50:
                canvas.clear_canvas()
                
            # Check if click is in the drawing mode area
            elif x > 130 and x < 230 and y < 40:
                new_mode = canvas.toggle_drawing_mode()
                print(f"Mode changed to: {'Drawing' if new_mode else 'Erasing'}")
                
            # Check if click is in the line mode area
            elif x > 230 and x < 330 and y < 40:
                new_mode = canvas.toggle_line_mode()
                print(f"Line mode changed to: {'Continuous' if new_mode else 'Dots'}")
                
            # Check if click is in the special effects area
            elif x > 330 and x < 430 and y < 40:
                new_effect = canvas.cycle_special_effect()
                effect_names = ["None", "Rainbow", "Glow"]
                print(f"Special effect changed to: {effect_names[new_effect]}")
                
            # Check if click is in the thickness display area - now does nothing
            elif x > self.frame_width - 300 and x < self.frame_width - 250 and y < 40:
                # This area now just displays the current size
                pass
                
            # Check if click is in the +/- area
            elif x > self.frame_width - 250 and x < self.frame_width - 225 and y < 40:
                # Left half of +/- button (decrease)
                new_thickness = canvas.adjust_brush_thickness(-1)
                print(f"Brush thickness decreased to: {new_thickness}")
            elif x > self.frame_width - 225 and x < self.frame_width - 200 and y < 40:
                # Right half of +/- button (increase)
                new_thickness = canvas.adjust_brush_thickness(1)
                print(f"Brush thickness increased to: {new_thickness}")
                
            # Check if click is in the color palette area
            for i in range(len(canvas.colors)):
                if x > 10 + i*30 and x < 30 + i*30 and y < 30:
                    canvas.set_color(i)
                    print(f"Color changed to: {canvas.color_names[i]}")
                    break
        
        return self.exit_program
    
    def combine_frame_and_canvas(self, frame, canvas):
        """
        Combine the video frame and drawing canvas.
        
        Args:
            frame (numpy.ndarray): Video frame
            canvas (numpy.ndarray): Drawing canvas
            
        Returns:
            numpy.ndarray: Combined output
        """
        return cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
    
    def print_instructions(self):
        """
        Print application instructions to the console.
        """
        print("\nAirDraw Controls:")
        print("--------------------")
        print("Click on the UI buttons to control the application")
        print("Click EXIT to quit")
        print("Click CLEAR to clear the canvas")
        print("Click on Mode to toggle between Draw and Erase")
        print("Click on Style to toggle between Line and Dots")
        print("Click on Effect to cycle through special effects")
        print("Click on colors to change drawing color")
        print("Click on +/- to adjust brush thickness\n") 