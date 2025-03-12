#!/usr/bin/env python3
"""
Reset Q-table for Air Tic Tac Toe.

This script deletes the existing Q-table file to start fresh.
"""

import os
import sys

def main():
    """Delete the Q-table file if it exists."""
    q_table_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tictactoe_q_table.pkl')
    
    if os.path.exists(q_table_path):
        try:
            os.remove(q_table_path)
            print(f"Successfully deleted Q-table file: {q_table_path}")
        except Exception as e:
            print(f"Error deleting Q-table file: {e}")
            return 1
    else:
        print(f"Q-table file not found at: {q_table_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 