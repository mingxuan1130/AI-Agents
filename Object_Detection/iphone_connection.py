#!/usr/bin/env python3
"""
iPhone Camera Connection Helper

This script is a convenience wrapper for the iPhone camera connection helper.
It imports and runs the main function from the src package.

Usage:
python iphone_connection.py

This will provide interactive instructions for connecting your iPhone camera
to your Mac for use with the object detection system.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main function from the src package
from iphone_connection import main

if __name__ == "__main__":
    main() 