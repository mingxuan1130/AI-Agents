#!/usr/bin/env python3
"""
Air Tic Tac Toe - Main Application

A game of Tic Tac Toe played in the air using hand gestures captured by a webcam.
"""

import cv2
import time
import numpy as np
from game_engine import TicTacToeGame
from rl_agent import TicTacToeRL
from gesture_detector import GestureDetector

class AirTicTacToe:
    """Main application class for Air Tic Tac Toe."""
    
    def __init__(self):
        """Initialize the application."""
        # Initialize webcam
        self.cap = cv2.VideoCapture(1)  # Try camera index 1 for MacBook Air camera
        
        # If camera index 1 fails, try camera index 0
        if not self.cap.isOpened():
            print("Camera index 1 failed, trying camera index 0...")
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                print("Error: Could not open any camera. Please check your camera connection.")
        
        # Initialize components
        self.game = TicTacToeGame()
        self.bot = TicTacToeRL()
        self.gesture_detector = GestureDetector()
        
        # Display parameters
        self.window_name = "Air Tic Tac Toe"
        cv2.namedWindow(self.window_name)
        
        # Interaction parameters
        self.active_cell = None
        
        # Player choice parameters
        self.show_menu = True
        self.player_goes_first = True
    
    def process_hand(self, hand_landmarks, frame):
        """
        Process hand landmarks for game interaction.
        
        Args:
            hand_landmarks: The hand landmarks
            frame (numpy.ndarray): The current frame
        """
        if self.game.game_over or self.game.current_player != 1:
            return
        
        # Get index finger tip position
        index_x, index_y = self.gesture_detector.get_finger_position(hand_landmarks, frame.shape)
        
        # Draw cursor at index finger tip
        cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), -1)
        
        # Get current cell
        current_cell = self.game.get_cell_from_position(index_x, index_y)
        
        # Update active cell
        self.active_cell = current_cell
        
        # Check for hover selection
        hover_selected = self.gesture_detector.check_hover(current_cell)
        
        # Draw hover feedback
        frame = self.gesture_detector.draw_hover_feedback(frame, current_cell, self.game)
        
        # Make move if hover selection is triggered
        if hover_selected and current_cell is not None:
            row, col = current_cell
            # Make move if valid
            if self.game.make_move(row, col, 1):
                # Let the bot learn from the outcome
                self.bot.learn_from_outcome(self.game.board, self.game.game_over, self.game.winner)
                
                # Switch to bot player if game not over
                if not self.game.game_over:
                    self.game.current_player = 2
    
    def bot_move(self):
        """Let the bot make a move."""
        if self.game.current_player != 2 or self.game.game_over:
            return
        
        try:
            # Small delay to make the bot's move visible
            time.sleep(0.5)
            
            # Get bot's move
            move = self.bot.make_move(self.game.board)
            
            if move:
                row, col = move
                self.game.make_move(row, col, 2)
                
                # Let the bot learn from the outcome
                self.bot.learn_from_outcome(self.game.board, self.game.game_over, self.game.winner)
        except Exception as e:
            print(f"Error during bot move: {e}")
            # If there's an error, just switch back to the player
            self.game.current_player = 1
    
    def draw_menu(self, frame):
        """
        Draw the menu screen for player to choose whether to go first or second.
        
        Args:
            frame (numpy.ndarray): The current frame
            
        Returns:
            numpy.ndarray: The frame with the menu drawn on it
        """
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Draw semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
        alpha = 0.7  # Transparency factor
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Draw title
        cv2.putText(frame, "Air Tic Tac Toe", (width//2 - 150, height//4), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Draw options
        option1_color = (0, 255, 0) if self.player_goes_first else (255, 255, 255)
        option2_color = (0, 255, 0) if not self.player_goes_first else (255, 255, 255)
        
        cv2.putText(frame, "1: Play First (X)", (width//2 - 120, height//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, option1_color, 2)
        cv2.putText(frame, "2: Play Second (O)", (width//2 - 120, height//2 + 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, option2_color, 2)
        
        # Draw instructions
        cv2.putText(frame, "Press '1' or '2' to select, then press 'Enter' to start", 
                   (width//2 - 250, height//2 + 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        return frame
    
    def process_menu_input(self, key):
        """
        Process keyboard input for the menu.
        
        Args:
            key (int): The key code
            
        Returns:
            bool: True if the menu should be closed, False otherwise
        """
        if key == ord('1'):
            self.player_goes_first = True
            return False
        elif key == ord('2'):
            self.player_goes_first = False
            return False
        elif key == 13:  # Enter key
            # Initialize the game based on player's choice
            self.game.reset_game()
            if not self.player_goes_first:
                self.game.current_player = 2  # Bot goes first
            return True
        return False
    
    def run(self):
        """Run the main application loop."""
        print("Starting Air Tic Tac Toe...")
        
        try:
            # Check if camera is opened successfully
            if not self.cap.isOpened():
                print("Error: Camera is not opened. Exiting...")
                return
                
            while True:
                # Read frame from webcam
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame from camera. Trying again...")
                    # Try to reinitialize the camera
                    self.cap.release()
                    self.cap = cv2.VideoCapture(1)
                    if not self.cap.isOpened():
                        self.cap = cv2.VideoCapture(0)
                    if not self.cap.isOpened():
                        print("Could not reconnect to any camera. Exiting...")
                        break
                    continue
                
                # Flip the frame horizontally for a more intuitive mirror view
                frame = cv2.flip(frame, 1)
                
                # Show menu if needed
                if self.show_menu:
                    frame = self.draw_menu(frame)
                    cv2.imshow(self.window_name, frame)
                    
                    # Check for key presses
                    key = cv2.waitKey(10) & 0xFF
                    if key == ord('q') or key == ord('Q'):
                        print("Quit key pressed. Exiting...")
                        break
                    
                    # Process menu input
                    if self.process_menu_input(key):
                        self.show_menu = False
                        # If bot goes first, make its move immediately
                        if not self.player_goes_first:
                            self.bot_move()
                    
                    continue
                
                # Process hand landmarks
                results = self.gesture_detector.process_frame(frame)
                
                # Draw the board
                frame = self.game.draw_board(frame)
                
                # Process hand if detected
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw hand landmarks
                        frame = self.gesture_detector.draw_landmarks(frame, hand_landmarks)
                        
                        # Process hand for game interaction
                        self.process_hand(hand_landmarks, frame)
                
                # Let bot make a move if it's its turn
                if self.game.current_player == 2 and not self.game.game_over:
                    self.bot_move()
                
                # Display the frame
                cv2.imshow(self.window_name, frame)
                
                # Check for key presses - use a shorter wait time to make key detection more responsive
                key = cv2.waitKey(10) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("Quit key pressed. Exiting...")
                    break
                elif key == ord('r') or key == ord('R'):
                    print("Reset key pressed. Restarting game...")
                    self.game.reset_game()
                    self.show_menu = True  # Show menu again for player to choose
        
        finally:
            # Clean up
            print("Cleaning up resources...")
            self.cap.release()
            cv2.destroyAllWindows()
            self.gesture_detector.close()
            
        print("Game ended. Goodbye!")

if __name__ == "__main__":
    app = AirTicTacToe()
    app.run() 