#!/usr/bin/env python3
"""
Real-time Object Detection System

This script is a convenience wrapper for the main object detection system.
It imports and runs the main function from the src package.

Usage:
1. Basic usage: python object_detector.py
2. Specify camera: python object_detector.py --camera 1
3. Specify API key: python object_detector.py --api-key "your-api-key"
4. Debug mode: python object_detector.py --debug
5. Manual detection mode: python object_detector.py --manual

For more information, see the README.md file.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main function from the src package
from main import main

if __name__ == "__main__":
    main() 