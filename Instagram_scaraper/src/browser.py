"""
Browser module for Instagram scraper.

This module contains functions for browser interaction and navigation.
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def connect_to_existing_browser():
    """
    Connect to an already-opened Chrome browser with remote debugging enabled.
    
    Returns:
        webdriver.Chrome: A Chrome WebDriver instance connected to the existing browser.
        
    Raises:
        Exception: If connection to the browser fails.
    """
    print("Attempting to connect to an existing Chrome window...")
    print("NOTE: Chrome must be already running with remote debugging enabled on port 9222.")
    
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        # Create a driver that connects to the existing browser
        driver = webdriver.Chrome(options=chrome_options)
        print("Successfully connected to Chrome")
        return driver
    except Exception as e:
        print(f"Failed to connect to Chrome: {e}")
        print("\nMake sure Chrome is running with remote debugging enabled.")
        print("You can start Chrome with remote debugging using the provided script:")
        print("bash start_chrome_for_scraping.sh")
        raise

def scroll_to_bottom(driver, scroll_pause_time=2, max_scrolls=20):
    """
    Scroll to the bottom of the page to load all images.
    
    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        scroll_pause_time (int, optional): Time to pause between scrolls in seconds. Defaults to 2.
        max_scrolls (int, optional): Maximum number of scrolls to perform. Defaults to 20.
    """
    print("Scrolling through the page to load all images...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0
    
    while scrolls < max_scrolls:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Add some randomness to appear more human-like
        time.sleep(scroll_pause_time + random.uniform(0.5, 1.5))
        
        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break if we've reached the bottom
        if new_height == last_height:
            break
            
        last_height = new_height
        scrolls += 1
        print(f"Scroll {scrolls}/{max_scrolls} completed")

def wait_for_instagram_page(driver, account_name="uchicago", max_wait_time=60):
    """
    Wait for the user to navigate to the specified Instagram account page.
    
    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        account_name (str, optional): The Instagram account name to wait for. Defaults to "uchicago".
        max_wait_time (int, optional): Maximum time to wait in seconds. Defaults to 60.
        
    Returns:
        bool: True if navigation was successful, False otherwise.
    """
    # Get the current URL to detect which account we're on
    current_url = driver.current_url
    print(f"Current URL: {current_url}")
    
    # Check if we're already on the Instagram page
    if f"instagram.com/{account_name}" in current_url:
        return True
    
    print(f"Please navigate to https://www.instagram.com/{account_name}/ in the Chrome browser")
    print(f"Waiting for navigation to the {account_name} Instagram page...")
    
    # Wait for the user to navigate to the correct page
    start_time = time.time()
    while f"instagram.com/{account_name}" not in driver.current_url:
        time.sleep(1)
        if time.time() - start_time > max_wait_time:
            print(f"Timeout waiting for navigation to {account_name} Instagram page.")
            print("Proceeding with current page anyway...")
            return False
        
        # Check if we're on the account page now
        if f"instagram.com/{account_name}" in driver.current_url:
            print(f"Detected navigation to {account_name} Instagram page!")
            return True
    
    return True 