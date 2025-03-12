#!/usr/bin/env python3
"""
API Key Validation Test

This script tests the validation of an OpenAI API key.
It's useful for verifying that your API key is working correctly
before using the object detection system.

Usage:
python test_api_key.py --api-key "your-api-key"
"""

import argparse
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import API utilities
from api_utils import validate_api_key, get_api_key

def main():
    """
    Main function to test API key validation.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test OpenAI API Key Validation')
    parser.add_argument('--api-key', type=str, help='OpenAI API key to test')
    args = parser.parse_args()
    
    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: OpenAI API key not provided.")
        print("Please provide an API key using the --api-key parameter or set the OPENAI_API_KEY environment variable.")
        return
    
    # Validate API key
    print(f"Testing API key: {api_key[:5]}...{api_key[-4:]} (key partially hidden for security)")
    is_valid, message = validate_api_key(api_key)
    
    # Print result
    if is_valid:
        print("\n✅ API key is valid and working correctly!")
        print(f"Message: {message}")
    else:
        print("\n❌ API key validation failed!")
        print(f"Error: {message}")
        print("\nPlease check your API key and try again.")

if __name__ == "__main__":
    main() 