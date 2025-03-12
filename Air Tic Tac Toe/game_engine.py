#!/usr/bin/env python3
"""
Game Engine for Air Tic Tac Toe.

This module contains the core game logic for the Tic Tac Toe game.
"""

import numpy as np
import cv2

class TicTacToeGame:
    """Core game logic for Tic Tac Toe."""
    
    def __init__(self):
        """Initialize the game state."""
        # Game state
        self.board = np.zeros((3, 3), dtype=int)  # 0: empty, 1: X, 2: O
        self.current_player = 1  # 1: X (human), 2: O (bot)
        self.game_over = False
        self.winner = None
        
        # Board display parameters
        self.board_size = 400
        self.cell_size = self.board_size // 3
        self.board_offset_x = 50  # Left offset
        self.board_offset_y = 50  # Top offset
    
    def reset_game(self):
        """Reset the game state to start a new game."""
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
    
    def check_winner(self):
        """Check if there's a winner or if the game is a draw."""
        # Check rows
        for row in range(3):
            if self.board[row, 0] != 0 and self.board[row, 0] == self.board[row, 1] == self.board[row, 2]:
                self.game_over = True
                self.winner = self.board[row, 0]
                return
        
        # Check columns
        for col in range(3):
            if self.board[0, col] != 0 and self.board[0, col] == self.board[1, col] == self.board[2, col]:
                self.game_over = True
                self.winner = self.board[0, col]
                return
        
        # Check diagonals
        if self.board[0, 0] != 0 and self.board[0, 0] == self.board[1, 1] == self.board[2, 2]:
            self.game_over = True
            self.winner = self.board[0, 0]
            return
        
        if self.board[0, 2] != 0 and self.board[0, 2] == self.board[1, 1] == self.board[2, 0]:
            self.game_over = True
            self.winner = self.board[0, 2]
            return
        
        # Check for draw
        if np.all(self.board != 0):
            self.game_over = True
            self.winner = 0  # Draw
            return
    
    def make_move(self, row, col, player):
        """
        Make a move on the board.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            player (int): Player number (1 for X, 2 for O)
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if self.game_over or not (0 <= row < 3 and 0 <= col < 3):
            return False
            
        if self.board[row, col] != 0:
            return False  # Cell already occupied
            
        self.board[row, col] = player
        self.check_winner()
        
        if not self.game_over:
            self.current_player = 3 - player  # Switch player (1->2, 2->1)
            
        return True
    
    def get_cell_from_position(self, x, y):
        """
        Convert screen coordinates to board cell.
        
        Args:
            x (int): X coordinate on screen
            y (int): Y coordinate on screen
            
        Returns:
            tuple: (row, col) if position is on board, None otherwise
        """
        # Check if position is within board
        if (self.board_offset_x <= x < self.board_offset_x + self.board_size and 
            self.board_offset_y <= y < self.board_offset_y + self.board_size):
            # Calculate cell
            cell_x = (x - self.board_offset_x) // self.cell_size
            cell_y = (y - self.board_offset_y) // self.cell_size
            return cell_y, cell_x  # Row, Col
        
        return None
    
    def draw_board(self, frame):
        """
        Draw the Tic Tac Toe board and pieces on the given frame.
        
        Args:
            frame (numpy.ndarray): The frame to draw on
            
        Returns:
            numpy.ndarray: The frame with the board drawn on it
        """
        # Draw board grid
        for i in range(1, 3):
            # Vertical lines
            cv2.line(frame, 
                    (self.board_offset_x + i * self.cell_size, self.board_offset_y), 
                    (self.board_offset_x + i * self.cell_size, self.board_offset_y + self.board_size), 
                    (255, 255, 255), 2)
            # Horizontal lines
            cv2.line(frame, 
                    (self.board_offset_x, self.board_offset_y + i * self.cell_size), 
                    (self.board_offset_x + self.board_size, self.board_offset_y + i * self.cell_size), 
                    (255, 255, 255), 2)
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                cell_center_x = self.board_offset_x + col * self.cell_size + self.cell_size // 2
                cell_center_y = self.board_offset_y + row * self.cell_size + self.cell_size // 2
                
                if self.board[row, col] == 1:  # X
                    offset = int(self.cell_size * 0.3)
                    cv2.line(frame, 
                            (cell_center_x - offset, cell_center_y - offset), 
                            (cell_center_x + offset, cell_center_y + offset), 
                            (0, 0, 255), 3)
                    cv2.line(frame, 
                            (cell_center_x + offset, cell_center_y - offset), 
                            (cell_center_x - offset, cell_center_y + offset), 
                            (0, 0, 255), 3)
                elif self.board[row, col] == 2:  # O
                    cv2.circle(frame, 
                              (cell_center_x, cell_center_y), 
                              int(self.cell_size * 0.3), 
                              (0, 255, 0), 3)
        
        # Display game status
        frame_height, frame_width = frame.shape[:2]
        status_text = ""
        if self.game_over:
            if self.winner == 0:
                status_text = "Game Over: Draw!"
            else:
                status_text = f"Game Over: {'X (You)' if self.winner == 1 else 'O (Bot)'} Wins!"
            cv2.putText(frame, status_text, (self.board_offset_x, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'R' to restart", (self.board_offset_x, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            status_text = f"Current Player: {'X (You)' if self.current_player == 1 else 'O (Bot)'}"
            cv2.putText(frame, status_text, (self.board_offset_x, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display instructions
        cv2.putText(frame, "Hover over a cell for 1 second to make a move", (10, frame_height - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Press 'Q' to quit", (10, frame_height - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                   
        return frame 