"""
iPhone Camera Connection Helper

This script provides detailed instructions for connecting an iPhone camera
to a Mac for use with the object detection system.
"""

import socket
import platform
import subprocess
import sys

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

def get_system_info():
    """
    Get system information.
    
    Returns:
        dict: System information
    """
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version.split()[0],
        "ip_address": get_ip_address()
    }
    
    # Get macOS version if on Mac
    if info["os"] == "Darwin":
        try:
            mac_version = subprocess.check_output(["sw_vers", "-productVersion"]).decode().strip()
            info["mac_version"] = mac_version
        except:
            info["mac_version"] = "Unknown"
    
    return info

def print_continuity_camera_instructions():
    """
    Print instructions for using Continuity Camera.
    """
    print("\n=== CONTINUITY CAMERA INSTRUCTIONS ===")
    print("Continuity Camera is the easiest way to use your iPhone as a webcam on Mac.")
    print("\nRequirements:")
    print("- Mac running macOS Ventura (13) or later")
    print("- iPhone running iOS 16 or later")
    print("- Both devices signed in to the same Apple ID")
    print("- Both devices have Bluetooth and Wi-Fi turned on")
    print("- Both devices are close to each other")
    
    print("\nSetup:")
    print("1. Make sure your iPhone is unlocked and near your Mac")
    print("2. Open an app that uses the camera on your Mac (like FaceTime or Photo Booth)")
    print("3. Click on the Video menu and select your iPhone")
    print("4. Your iPhone should automatically activate as a camera")
    
    print("\nUsing with Object Detector:")
    print("1. Run the object detector with camera index 1:")
    print("   python main.py --camera 1")
    print("2. If that doesn't work, try other indices (0, 2, etc.):")
    print("   python main.py --camera 0")
    print("   python main.py --camera 2")
    
    print("\nTroubleshooting:")
    print("- Make sure both devices are signed in to the same Apple ID")
    print("- Make sure both devices have Bluetooth and Wi-Fi turned on")
    print("- Restart both devices")
    print("- Check Apple's support page: https://support.apple.com/en-us/HT213244")

def print_camo_instructions():
    """
    Print instructions for using Camo.
    """
    print("\n=== CAMO APP INSTRUCTIONS ===")
    print("Camo provides high-quality iPhone camera streaming to Mac.")
    
    print("\nSetup:")
    print("1. Install Camo on your iPhone from the App Store:")
    print("   https://apps.apple.com/app/camo-webcam-for-mac-and-pc/id1514199064")
    print("2. Install Camo Studio on your Mac:")
    print("   https://reincubate.com/camo/")
    print("3. Connect your iPhone to your Mac with a cable")
    print("4. Open Camo on both devices")
    print("5. Camo Studio should detect your iPhone automatically")
    
    print("\nUsing with Object Detector:")
    print("1. Make sure Camo Studio is running and connected to your iPhone")
    print("2. Run the object detector with camera index 1:")
    print("   python main.py --camera 1")
    print("3. If that doesn't work, try other indices:")
    print("   python main.py --camera 2")
    
    print("\nTroubleshooting:")
    print("- Make sure Camo is running on both devices")
    print("- Try disconnecting and reconnecting the cable")
    print("- Restart Camo on both devices")
    print("- Check Camo's support page: https://reincubate.com/support/camo/")

def print_ip_camera_instructions():
    """
    Print instructions for using an IP camera app.
    """
    ip_address = get_ip_address()
    
    print("\n=== IP CAMERA APP INSTRUCTIONS ===")
    print("You can use various IP camera apps to stream your iPhone camera over Wi-Fi.")
    
    print("\nRecommended Apps:")
    print("- IP Camera Lite (iOS App Store)")
    print("- DroidCam (iOS App Store)")
    print("- EpocCam (iOS App Store)")
    
    print("\nGeneral Setup:")
    print("1. Install an IP camera app on your iPhone")
    print("2. Connect your iPhone to the same Wi-Fi network as your Mac")
    print(f"3. Your Mac's IP address is: {ip_address}")
    print("4. Open the app and start the camera server")
    print("5. Note the URL provided by the app (usually shown on screen)")
    
    print("\nUsing with Object Detector:")
    print("1. Run the object detector with the URL:")
    print("   python main.py --url http://iPhone-IP-Address:Port/video")
    print("   For example:")
    print("   python main.py --url http://192.168.1.100:8080/video")
    
    print("\nTroubleshooting:")
    print("- Make sure both devices are on the same Wi-Fi network")
    print("- Check if there's a firewall blocking the connection")
    print("- Try using a different port if provided by the app")
    print("- Consult the specific app's documentation for the correct URL format")

def main():
    """
    Main function to display iPhone camera connection instructions.
    """
    system_info = get_system_info()
    
    print("\n==================================================")
    print("  IPHONE CAMERA CONNECTION HELPER")
    print("==================================================")
    
    print("\nSystem Information:")
    print(f"Operating System: {system_info['os']}")
    if system_info['os'] == "Darwin":
        print(f"macOS Version: {system_info.get('mac_version', 'Unknown')}")
    print(f"Python Version: {system_info['python_version']}")
    print(f"IP Address: {system_info['ip_address']}")
    
    print("\nThis helper provides instructions for connecting your iPhone camera to your Mac.")
    print("There are three main methods to connect your iPhone camera:")
    print("1. Continuity Camera (easiest for Mac+iPhone)")
    print("2. Camo App (high quality, requires cable)")
    print("3. IP Camera App (wireless, requires same Wi-Fi)")
    
    while True:
        print("\nWhich method would you like instructions for?")
        print("1. Continuity Camera")
        print("2. Camo App")
        print("3. IP Camera App")
        print("4. All Methods")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            print_continuity_camera_instructions()
        elif choice == "2":
            print_camo_instructions()
        elif choice == "3":
            print_ip_camera_instructions()
        elif choice == "4":
            print_continuity_camera_instructions()
            print_camo_instructions()
            print_ip_camera_instructions()
        elif choice == "5":
            print("\nExiting iPhone Camera Connection Helper.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main() 