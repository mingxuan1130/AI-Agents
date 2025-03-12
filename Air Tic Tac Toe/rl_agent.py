#!/usr/bin/env python3
"""
Reinforcement Learning Agent for Air Tic Tac Toe.

This module contains the RL agent that learns to play Tic Tac Toe.
"""

import os
import pickle
import random
import numpy as np
from collections import defaultdict

# Create a nested defaultdict that works for any depth
def nested_defaultdict():
    """Create a nested defaultdict that returns 0.0 for missing keys at any depth."""
    return defaultdict(float)

class TicTacToeRL:
    """Reinforcement Learning agent for Tic Tac Toe."""
    
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        """
        Initialize the RL agent.
        
        Args:
            epsilon (float): Exploration rate (0-1)
            alpha (float): Learning rate (0-1)
            gamma (float): Discount factor (0-1)
        """
        # RL parameters
        self.epsilon = epsilon  # exploration rate
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        
        # Load Q-table if exists, otherwise create a new one
        self.q_table_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tictactoe_q_table.pkl')
        
        # Initialize a new Q-table with proper nesting
        self.q_table = defaultdict(nested_defaultdict)
        
        if os.path.exists(self.q_table_file):
            try:
                with open(self.q_table_file, 'rb') as f:
                    loaded_q_table = pickle.load(f)
                    # Convert the loaded dictionary to our defaultdict structure
                    for state, actions in loaded_q_table.items():
                        for action, value in actions.items():
                            self.q_table[state][action] = value
                print("Loaded Q-table from file")
            except Exception as e:
                print(f"Error loading Q-table: {e}")
                # Already initialized above
        else:
            print("Created new Q-table")
        
        # Game state
        self.last_state = None
        self.last_action = None
        
        # Strategy parameters
        self.use_minimax = True  # Set to True to use minimax algorithm
        self.minimax_depth = 9   # Maximum depth for minimax search
        self.adaptive_epsilon = True  # Dynamically adjust epsilon based on game progress
    
    def board_to_state(self, board):
        """
        Convert board to a hashable state representation.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            tuple: A hashable representation of the board
        """
        return tuple(map(tuple, board))
    
    def get_valid_actions(self, board):
        """
        Get all valid moves (empty cells).
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            list: List of valid moves as (row, col) tuples
        """
        valid_actions = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    valid_actions.append((i, j))
        return valid_actions
    
    def choose_action(self, board):
        """
        Choose an action using epsilon-greedy policy.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            tuple: The chosen action as (row, col)
        """
        state = self.board_to_state(board)
        valid_actions = self.get_valid_actions(board)
        
        if not valid_actions:
            return None  # No valid moves
        
        # Calculate number of empty cells to adjust exploration rate
        empty_cells = sum(1 for i in range(3) for j in range(3) if board[i][j] == 0)
        
        # Adaptive epsilon: reduce exploration as the game progresses
        current_epsilon = self.epsilon
        if self.adaptive_epsilon:
            # Start with higher exploration and decrease as the game progresses
            current_epsilon = self.epsilon * (empty_cells / 9.0)
        
        # Try minimax first if enabled
        if self.use_minimax and random.random() > current_epsilon:
            minimax_action = self.minimax_decision(board)
            if minimax_action:
                return minimax_action
        
        # Exploration: random move
        if random.random() < current_epsilon:
            return random.choice(valid_actions)
        
        # Exploitation: best known move
        # With defaultdict, we don't need to worry about KeyError
        q_values = {action: self.q_table[state][action] for action in valid_actions}
        
        # If all values are 0 (default), choose randomly
        if all(value == 0 for value in q_values.values()):
            # Check for strategic moves before falling back to random
            strategic_move = self.get_strategic_move(board)
            if strategic_move:
                return strategic_move
            return random.choice(valid_actions)
            
        max_q = max(q_values.values())
        
        # If multiple actions have the same max Q-value, choose randomly among them
        best_actions = [action for action, q_value in q_values.items() if q_value == max_q]
        return random.choice(best_actions)
    
    def get_strategic_move(self, board):
        """
        Get a strategic move based on common Tic Tac Toe strategies.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            tuple or None: A strategic move or None if no strategic move is found
        """
        # Check if we can win in the next move
        for action in self.get_valid_actions(board):
            row, col = action
            board_copy = board.copy()
            board_copy[row, col] = 2  # Bot's move
            if self.check_winner(board_copy) == 2:
                return action
        
        # Check if we need to block the opponent from winning
        for action in self.get_valid_actions(board):
            row, col = action
            board_copy = board.copy()
            board_copy[row, col] = 1  # Human's move
            if self.check_winner(board_copy) == 1:
                return action
        
        # Take center if available
        if board[1, 1] == 0:
            return (1, 1)
        
        # Take corners if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if board[corner[0], corner[1]] == 0]
        if available_corners:
            return random.choice(available_corners)
        
        # No strategic move found
        return None
    
    def check_winner(self, board):
        """
        Check if there's a winner on the board.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            int: 0 for no winner, 1 for player 1, 2 for player 2
        """
        # Check rows
        for row in range(3):
            if board[row, 0] != 0 and board[row, 0] == board[row, 1] == board[row, 2]:
                return board[row, 0]
        
        # Check columns
        for col in range(3):
            if board[0, col] != 0 and board[0, col] == board[1, col] == board[2, col]:
                return board[0, col]
        
        # Check diagonals
        if board[0, 0] != 0 and board[0, 0] == board[1, 1] == board[2, 2]:
            return board[0, 0]
        
        if board[0, 2] != 0 and board[0, 2] == board[1, 1] == board[2, 0]:
            return board[0, 2]
        
        return 0  # No winner
    
    def is_terminal(self, board):
        """
        Check if the game is over.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            bool: True if the game is over, False otherwise
        """
        # Check for winner
        if self.check_winner(board) != 0:
            return True
        
        # Check for draw
        return np.all(board != 0)
    
    def evaluate(self, board):
        """
        Evaluate the board state for minimax.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            int: Score of the board state
        """
        winner = self.check_winner(board)
        
        if winner == 2:  # Bot wins
            return 10
        elif winner == 1:  # Human wins
            return -10
        else:  # Draw or ongoing
            return 0
    
    def minimax(self, board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board (numpy.ndarray): The game board
            depth (int): Current depth in the search tree
            is_maximizing (bool): Whether it's the maximizing player's turn
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            
        Returns:
            tuple: (best_score, best_move)
        """
        # Check terminal state
        if self.is_terminal(board) or depth == 0:
            return self.evaluate(board), None
        
        valid_actions = self.get_valid_actions(board)
        if not valid_actions:
            return 0, None  # Draw
        
        best_move = None
        
        if is_maximizing:  # Bot's turn (maximizing)
            best_score = -float('inf')
            for action in valid_actions:
                row, col = action
                board_copy = board.copy()
                board_copy[row, col] = 2  # Bot's move
                
                score, _ = self.minimax(board_copy, depth - 1, False, alpha, beta)
                
                if score > best_score:
                    best_score = score
                    best_move = action
                
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cutoff
        else:  # Human's turn (minimizing)
            best_score = float('inf')
            for action in valid_actions:
                row, col = action
                board_copy = board.copy()
                board_copy[row, col] = 1  # Human's move
                
                score, _ = self.minimax(board_copy, depth - 1, True, alpha, beta)
                
                if score < best_score:
                    best_score = score
                    best_move = action
                
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cutoff
        
        return best_score, best_move
    
    def minimax_decision(self, board):
        """
        Make a decision using the minimax algorithm.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            tuple: The best move as (row, col)
        """
        # Calculate remaining empty cells to determine search depth
        empty_cells = sum(1 for i in range(3) for j in range(3) if board[i][j] == 0)
        
        # Adjust depth based on number of empty cells
        depth = min(empty_cells, self.minimax_depth)
        
        _, best_move = self.minimax(board, depth, True)
        return best_move
    
    def update_q_table(self, state, action, reward, next_state, done):
        """
        Update Q-table using Q-learning algorithm.
        
        Args:
            state (tuple): Current state
            action (tuple): Action taken
            reward (float): Reward received
            next_state (tuple): Next state
            done (bool): Whether the episode is done
        """
        if action is None:
            return
        
        # Convert action to tuple if it's not already
        if not isinstance(action, tuple):
            action = tuple(action)
        
        # Current Q-value
        current_q = self.q_table[state][action]
        
        if done:
            # Terminal state
            new_q = current_q + self.alpha * (reward - current_q)
        else:
            # Non-terminal state
            next_actions = self.get_valid_actions(np.array(next_state).reshape(3, 3))
            
            # Handle the case where there are no next actions
            if next_actions:
                # With defaultdict, we don't need to worry about KeyError
                max_next_q = max(self.q_table[next_state][a] for a in next_actions)
            else:
                max_next_q = 0
            
            new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        
        self.q_table[state][action] = new_q
    
    def make_move(self, board):
        """
        Make a move and remember the state and action.
        
        Args:
            board (numpy.ndarray): The game board
            
        Returns:
            tuple: The chosen action as (row, col)
        """
        self.last_state = self.board_to_state(board)
        self.last_action = self.choose_action(board)
        return self.last_action
    
    def learn_from_outcome(self, board, game_over, winner):
        """
        Learn from the game outcome.
        
        Args:
            board (numpy.ndarray): The current game board
            game_over (bool): Whether the game is over
            winner (int): The winner (0 for draw, 1 for player 1, 2 for player 2)
        """
        if self.last_state is None or self.last_action is None:
            return
        
        current_state = self.board_to_state(board)
        
        # Enhanced reward function
        if game_over:
            if winner == 2:  # Bot wins
                reward = 1.0
            elif winner == 1:  # Human wins
                reward = -1.0
            else:  # Draw
                # Draw is better than losing but worse than winning
                reward = 0.5
        else:
            # Intermediate state rewards based on board position
            board_array = np.array(current_state)
            
            # Count potential winning lines for bot
            bot_potential = self.count_potential_wins(board_array, 2)
            
            # Count potential winning lines for human
            human_potential = self.count_potential_wins(board_array, 1)
            
            # Reward is proportional to bot's advantage
            reward = 0.05 * (bot_potential - human_potential)
        
        # Update Q-table
        self.update_q_table(self.last_state, self.last_action, reward, current_state, game_over)
        
        # Save Q-table periodically
        if game_over:
            try:
                # Convert defaultdict to regular dict for pickling
                q_table_dict = {k: dict(v) for k, v in self.q_table.items()}
                with open(self.q_table_file, 'wb') as f:
                    pickle.dump(q_table_dict, f)
                print("Saved Q-table to file")
            except Exception as e:
                print(f"Error saving Q-table: {e}")
    
    def count_potential_wins(self, board, player):
        """
        Count the number of potential winning lines for a player.
        
        Args:
            board (numpy.ndarray): The game board
            player (int): The player to check for (1 or 2)
            
        Returns:
            int: Number of potential winning lines
        """
        opponent = 3 - player  # Other player
        count = 0
        
        # Check rows
        for row in range(3):
            if opponent not in board[row, :] and player in board[row, :]:
                count += 1
        
        # Check columns
        for col in range(3):
            if opponent not in board[:, col] and player in board[:, col]:
                count += 1
        
        # Check diagonals
        diag1 = [board[0, 0], board[1, 1], board[2, 2]]
        if opponent not in diag1 and player in diag1:
            count += 1
        
        diag2 = [board[0, 2], board[1, 1], board[2, 0]]
        if opponent not in diag2 and player in diag2:
            count += 1
        
        return count 