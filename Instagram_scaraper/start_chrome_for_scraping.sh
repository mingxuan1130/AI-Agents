#!/bin/bash
# Script to start Chrome with remote debugging enabled for Instagram scraping

echo "Starting Chrome with remote debugging enabled on port 9222..."
echo "After Chrome opens, navigate to the Instagram account you want to scrape."
echo "Then run the script with: python instagram_scraper.py --account <account_name>"

# Create a temporary profile directory
TEMP_PROFILE_DIR="/tmp/chrome_debug_profile"

# Check if we're on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS path
    CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if [ ! -f "$CHROME_PATH" ]; then
        echo "Chrome not found at $CHROME_PATH"
        echo "Please install Chrome or update the path in this script."
        exit 1
    fi
    
    # Start Chrome with remote debugging
    "$CHROME_PATH" --remote-debugging-port=9222 --user-data-dir="$TEMP_PROFILE_DIR"
else
    # Linux/Windows path (assuming Chrome is in PATH)
    if command -v google-chrome &> /dev/null; then
        google-chrome --remote-debugging-port=9222 --user-data-dir="$TEMP_PROFILE_DIR"
    elif command -v chrome &> /dev/null; then
        chrome --remote-debugging-port=9222 --user-data-dir="$TEMP_PROFILE_DIR"
    else
        echo "Chrome not found in PATH."
        echo "Please install Chrome or make sure it's in your PATH."
        exit 1
    fi
fi 