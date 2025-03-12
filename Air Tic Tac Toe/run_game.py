#!/usr/bin/env python3
"""
Run Air Tic Tac Toe Game

This script provides a simple way to start the game with error handling.
"""

import os
import sys
import traceback

def main():
    """Run the Air Tic Tac Toe game."""
    try:
        # Import the main module
        from main import AirTicTacToe
        
        # Create and run the game
        print("Starting Air Tic Tac Toe...")
        app = AirTicTacToe()
        app.run()
        
        return 0
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure you're running this script from the Air Tic Tac Toe directory.")
        return 1
    except Exception as e:
        print(f"Error running the game: {e}")
        print("\nDetailed error information:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 