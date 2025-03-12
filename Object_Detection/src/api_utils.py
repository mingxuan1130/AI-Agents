"""
API Utilities Module

This module provides utilities for API key validation and testing.
"""

import os
from openai import OpenAI

def validate_api_key(api_key):
    """
    Validate an OpenAI API key by making a test request.
    
    Args:
        api_key (str): OpenAI API key to validate
        
    Returns:
        bool: True if API key is valid, False otherwise
        str: Status message
    """
    print("Testing API key...")
    
    if not api_key:
        return False, "No API key provided"
    
    if not api_key.startswith("sk-"):
        return False, "Invalid API key format. API key should start with 'sk-'"
    
    try:
        # Set environment variable
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize client
        try:
            client = OpenAI()  # Using environment variable
            print("Initializing test client using environment variable")
        except Exception as e:
            print(f"Failed to initialize client using environment variable: {e}")
            client = OpenAI(api_key=api_key)
            print("Falling back to direct API key")
            
        # Make a simple test request
        test_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API key is working!' in English"}
            ]
        )
        
        response_text = test_response.choices[0].message.content
        print(f"API key test successful: {response_text}")
        
        return True, "API key is valid"
        
    except Exception as e:
        error_message = f"API key validation failed: {str(e)}"
        print(f"Warning: {error_message}")
        return False, error_message

def get_api_key(provided_key=None):
    """
    Get an OpenAI API key from various sources.
    
    Priority order:
    1. Provided key parameter
    2. Environment variable
    
    Args:
        provided_key (str): API key provided as parameter
        
    Returns:
        str: API key or None if not found
    """
    # Check provided key
    if provided_key:
        return provided_key
        
    # Check environment variable
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
        
    # No key found
    return None 