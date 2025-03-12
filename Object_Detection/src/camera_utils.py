"""
Camera Utilities Module

This module provides utilities for camera connection and management,
particularly for connecting to iPhone cameras.
"""

import socket
import cv2

def get_ip_address():
    """
    Get the local IP address of the machine.
    
    Returns:
        str: Local IP address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def suggest_camera_connection():
    """
    Print suggestions for iPhone camera connection.
    
    This function provides guidance on different methods to connect
    an iPhone camera to a Mac for use with the object detection system.
    """
    ip_address = get_ip_address()
    
    print("\n===== IPHONE CAMERA CONNECTION =====")
    print("\nIf you haven't connected your iPhone camera yet, try one of these methods:")
    print("\n1. Use Continuity Camera (easiest for Mac+iPhone):")
    print("   - Make sure your Mac is running macOS Ventura or later")
    print("   - Make sure your iPhone and Mac are using the same Apple ID")
    print("   - Your iPhone should automatically appear as a camera option")
    
    print("\n2. Use Camo app:")
    print("   - Install Camo on iPhone and Camo Studio on Mac")
    print("   - Connect iPhone to Mac with a cable")
    print("   - Run this script with camera index 1")
    
    print("\n3. Use a network camera app:")
    print("   - Install a camera streaming app on your iPhone")
    print(f"   - Your Mac's IP address is: {ip_address}")
    print("   - In the app, set up streaming and note the URL")
    print("   - Run this script with the --url parameter")
    
    print("\nFor more detailed instructions, run:")
    print("python iphone_connection.py")
    print("===================================\n")

def open_camera(camera_index=0, camera_url=None):
    """
    Open a camera for video capture.
    
    Args:
        camera_index (int): Index of the camera to open (default: 0)
        camera_url (str): URL of IP camera (if provided, overrides camera_index)
        
    Returns:
        cv2.VideoCapture: Video capture object
        bool: Success status
    """
    print("Opening camera...")
    
    if camera_url:
        print(f"Connecting to IP camera: {camera_url}")
        cap = cv2.VideoCapture(camera_url)
    else:
        print(f"Opening local camera (index {camera_index})...")
        cap = cv2.VideoCapture(camera_index)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to use provided settings to open camera.")
        suggest_camera_connection()
        return cap, False
    
    # Get actual frame dimensions
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video frame. Please check your camera.")
        cap.release()
        suggest_camera_connection()
        return cap, False
    
    print(f"Camera opened successfully. Resolution: {frame.shape[1]}x{frame.shape[0]}")
    return cap, True 