# Air Tic Tac Toe

A Python application that allows users to play Tic Tac Toe in the air using hand gestures captured by a webcam.

## Overview

Air Tic Tac Toe uses computer vision to track hand movements and allows players to make moves in a virtual Tic Tac Toe board by drawing "X" gestures in the air. The game features an advanced AI bot that combines reinforcement learning with minimax algorithm to provide a challenging opponent.

## Features

- Draw X gestures in the air to make moves
- Play against an intelligent AI bot that uses multiple strategies
- Choose whether to play first (X) or second (O)
- Visual feedback for gesture detection
- Automatic camera selection (works with built-in or external webcams)
- Modular, well-organized code structure

## Requirements

- Python 3.8+
- OpenCV
- NumPy
- MediaPipe (for hand tracking)

## Project Structure

The project is organized into several modules:

- `main.py`: The main application entry point
- `game_engine.py`: Core game logic for Tic Tac Toe
- `gesture_detector.py`: Hand gesture detection and processing
- `rl_agent.py`: Advanced AI agent combining reinforcement learning and minimax
- `tictactoe_q_table.pkl`: Saved learning data for the bot (created automatically)

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the game with either:
```
python main.py
```

Or use the simplified run script with better error handling:
```
python run_game.py
```

If you want to reset the bot's learning data:
```
python reset_q_table.py
```

## How to Play

1. When the game starts, you'll see a menu screen where you can choose to:
   - Press '1' to play first (X)
   - Press '2' to play second (O)
   - Press 'Enter' to confirm your selection
2. Position yourself in front of the webcam
3. Use your index finger to draw an "X" gesture over the cell where you want to place your mark
4. The bot will automatically make its move after you
5. Continue until someone wins or the game is a draw
6. Press 'R' to restart the game or 'Q' to quit

## Gesture Detection

The game detects "X" gestures by tracking your index finger movement. To make a successful X gesture:

1. Extend your index finger (keep other fingers folded)
2. Draw an X shape over the cell where you want to place your mark
3. A green circle and "X Gesture Detected!" message will appear when the gesture is recognized

## Advanced AI Bot

The game features a sophisticated AI bot that combines multiple techniques to provide a challenging opponent:

### Minimax Algorithm with Alpha-Beta Pruning
- The bot uses the minimax algorithm to look ahead and consider all possible future game states
- Alpha-beta pruning is implemented to efficiently search through possible moves
- This allows the bot to play optimally in most situations

### Strategic Knowledge
- The bot has explicit strategic knowledge about Tic Tac Toe
- It will immediately take winning moves when available
- It will block your winning moves
- It prioritizes the center square, which is strategically valuable
- It prefers corner squares over edge squares when no better move is available

### Reinforcement Learning (Q-Learning)
- The bot continues to learn from each game through Q-learning
- It receives rewards for winning and penalties for losing
- The learning data is saved between sessions in the `tictactoe_q_table.pkl` file
- The more you play, the better the bot becomes at adapting to your play style

### Adaptive Exploration
- The bot uses adaptive exploration to balance between trying new strategies and using proven ones
- It explores more in the early game when there are more options
- It becomes more focused on exploitation as the game progresses
- This helps it learn more effectively while still playing well

### Hybrid Approach
- The bot uses a hybrid approach that combines the strengths of different AI techniques
- Minimax for perfect play when enabled
- Q-learning as a fallback and for learning from experience
- Strategic heuristics when neither has a clear preference

## Adjusting Bot Difficulty

You can adjust the bot's difficulty by modifying these parameters in the `rl_agent.py` file:
- `self.use_minimax = True` - Set to False for an easier bot
- `self.epsilon = 0.1` - Increase for more random play (easier)
- `self.adaptive_epsilon = True` - Set to False for consistent exploration 