import cv2
import numpy as np
import math
import colorsys
from collections import deque

class DrawingCanvas:
    """
    A class for managing the drawing canvas and drawing operations.
    Provides functionality for different drawing modes, effects, and styles.
    """
    
    def __init__(self, frame_width, frame_height):
        """
        Initialize the drawing canvas with specified dimensions.
        
        Args:
            frame_width (int): Width of the canvas
            frame_height (int): Height of the canvas
        """
        # Create canvas with the same dimensions as the frame
        self.canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Define color palette
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (128, 0, 128)]  # Blue, Green, Red, Yellow, Magenta, Purple
        self.color_names = ["Blue", "Green", "Red", "Yellow", "Magenta", "Purple"]
        self.current_color_idx = 0
        self.current_color = self.colors[self.current_color_idx]
        
        # Define brush thickness
        self.brush_thickness = 5
        
        # Define drawing variables
        self.drawing_mode = True  # True for drawing, False for erasing
        self.line_mode = True  # True for continuous lines, False for dots
        self.drawing_points = deque(maxlen=1024)
        self.prev_point = None
        
        # Special effects
        self.special_effect = 0  # 0: None, 1: Rainbow, 2: Glow
        self.rainbow_index = 0
    
    def clear_canvas(self):
        """
        Clear the entire canvas.
        """
        self.canvas[:] = 0
        self.drawing_points.clear()
        self.prev_point = None
    
    def set_color(self, color_idx):
        """
        Set the current drawing color.
        
        Args:
            color_idx (int): Index of the color in the color palette
        """
        if 0 <= color_idx < len(self.colors):
            self.current_color_idx = color_idx
            self.current_color = self.colors[self.current_color_idx]
    
    def toggle_drawing_mode(self):
        """
        Toggle between drawing and erasing modes.
        
        Returns:
            bool: The new drawing mode
        """
        self.drawing_mode = not self.drawing_mode
        return self.drawing_mode
    
    def toggle_line_mode(self):
        """
        Toggle between continuous line and dot drawing styles.
        
        Returns:
            bool: The new line mode
        """
        self.line_mode = not self.line_mode
        return self.line_mode
    
    def cycle_special_effect(self):
        """
        Cycle through available special effects.
        
        Returns:
            int: The new special effect index
        """
        self.special_effect = (self.special_effect + 1) % 3
        return self.special_effect
    
    def adjust_brush_thickness(self, delta):
        """
        Adjust the brush thickness.
        
        Args:
            delta (int): Amount to change the thickness by
            
        Returns:
            int: The new brush thickness
        """
        self.brush_thickness = max(1, min(20, self.brush_thickness + delta))
        return self.brush_thickness
    
    def rainbow_color(self):
        """
        Generate a color from the rainbow spectrum.
        
        Returns:
            tuple: (B, G, R) color values
        """
        self.rainbow_index = (self.rainbow_index + 1) % 360
        hue = self.rainbow_index / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        return (b, g, r)  # OpenCV uses BGR
    
    def get_current_draw_color(self):
        """
        Get the current drawing color, considering special effects.
        
        Returns:
            tuple: (B, G, R) color values
        """
        if self.special_effect == 1:  # Rainbow effect
            return self.rainbow_color()
        return self.current_color
    
    def draw_point(self, x, y, is_drawing, current_time):
        """
        Draw a point or line on the canvas.
        
        Args:
            x (int): X-coordinate
            y (int): Y-coordinate
            is_drawing (bool): Whether drawing is active
            current_time (float): Current time for special effects
            
        Returns:
            tuple: Updated previous point
        """
        if not is_drawing:
            return self.prev_point
        
        draw_color = self.get_current_draw_color()
        
        if self.drawing_mode:
            # Handle line mode vs dot mode
            if self.line_mode and self.prev_point is not None:
                # Draw line between previous point and current point
                cv2.line(self.canvas, self.prev_point, (x, y), draw_color, self.brush_thickness)
                
                # For glow effect, draw additional circles along the line
                if self.special_effect == 2:  # Glow effect
                    # Calculate number of points to draw based on distance
                    dist = math.sqrt((self.prev_point[0] - x)**2 + (self.prev_point[1] - y)**2)
                    steps = max(1, int(dist / 5))
                    
                    for i in range(1, steps):
                        ix = int(self.prev_point[0] + (x - self.prev_point[0]) * i / steps)
                        iy = int(self.prev_point[1] + (y - self.prev_point[1]) * i / steps)
                        # Draw glow circles with varying sizes
                        glow_radius = self.brush_thickness + 3 * math.sin(current_time * 5 + i / 2)
                        cv2.circle(self.canvas, (ix, iy), int(glow_radius), draw_color, -1)
                
                self.drawing_points.append((x, y, draw_color, self.brush_thickness))
            else:
                # Just draw a dot at the current position
                cv2.circle(self.canvas, (x, y), self.brush_thickness, draw_color, -1)
                self.drawing_points.append((x, y, draw_color, self.brush_thickness))
        else:  # Erasing mode
            # Create a black circle for erasing
            cv2.circle(self.canvas, (x, y), self.brush_thickness * 2, (0, 0, 0), -1)
            
            # Also remove points from the drawing queue that are near the eraser
            for i in range(len(self.drawing_points)):
                px, py, _, _ = self.drawing_points[i]
                # If the eraser is close to a drawn point, remove it
                if abs(x - px) < self.brush_thickness * 2 and abs(y - py) < self.brush_thickness * 2:
                    self.drawing_points[i] = (px, py, (0, 0, 0), 0)  # Mark for removal
        
        return (x, y)
    
    def redraw_points(self):
        """
        Redraw all points in the drawing queue.
        Used for dot mode or special effects that need redrawing.
        """
        if not self.line_mode or self.special_effect == 2:
            for point in self.drawing_points:
                x, y, color, thickness = point
                if thickness > 0:  # Skip points marked for removal
                    cv2.circle(self.canvas, (x, y), thickness, color, -1)
    
    def get_canvas(self):
        """
        Get the current canvas.
        
        Returns:
            numpy.ndarray: The current canvas
        """
        return self.canvas 