# Real-time Object Detection with GPT-4o Vision

This project provides a real-time object detection system using OpenAI's GPT-4o Vision API and your camera (with special support for iPhone cameras on Mac). The system detects objects in the camera feed, draws bounding boxes around them, and labels each object with its name and confidence score.

## Features

- **Real-time Object Detection**: Identify objects in your camera feed using OpenAI's powerful GPT-4o Vision model
- **iPhone Camera Support**: Seamlessly connect your iPhone camera to your Mac using Apple's Continuity Camera feature
- **Multiple Connection Methods**: Support for various iPhone camera connection methods (Continuity Camera, Camo, IP Camera apps)
- **Visual Feedback**: Color-coded bounding boxes and labels for different object categories
- **Flexible Controls**: Toggle between automatic and manual detection modes
- **Confidence Filtering**: Only show detections above a configurable confidence threshold

## Requirements

- Python 3.7 or later
- OpenAI API key with access to GPT-4o
- Webcam or iPhone camera
- For iPhone camera on Mac:
  - macOS Ventura (13) or later
  - iPhone with iOS 16 or later
  - Both devices signed in to the same Apple ID

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Obtain an OpenAI API key with access to GPT-4o

## Usage

### Basic Usage

```bash
python object_detector.py --api-key "your-api-key"
```

### Specify a Camera

```bash
python object_detector.py --camera 1 --api-key "your-api-key"
```

This will use the camera with index 1 (often the external/iPhone camera).

### Use a Network Camera

```bash
python object_detector.py --url http://192.168.1.100:8080/video --api-key "your-api-key"
```

Replace the URL with the one provided by your iPhone camera app.

### Manual Detection Mode

```bash
python object_detector.py --manual --api-key "your-api-key"
```

This starts the system in manual detection mode, where you need to press the space bar to trigger detection.

### Debug Mode

```bash
python object_detector.py --debug --api-key "your-api-key"
```

This enables additional debug information.

## iPhone Camera Connection

This project includes special support for connecting your iPhone camera to your Mac. There are three main methods:

### 1. Continuity Camera (Recommended)

Apple's Continuity Camera feature allows you to use your iPhone as a webcam on your Mac wirelessly:

- Make sure your Mac is running macOS Ventura (13) or later
- Make sure your iPhone is running iOS 16 or later
- Both devices must be signed in to the same Apple ID
- Both devices must have Bluetooth and Wi-Fi turned on
- Your iPhone should automatically appear as a camera option

### 2. Camo App

Camo provides high-quality video with many configuration options:

- Install [Camo](https://apps.apple.com/app/camo-webcam-for-mac-and-pc/id1514199064) on your iPhone
- Install [Camo Studio](https://reincubate.com/camo/) on your Mac
- Connect your iPhone to your Mac with a cable
- Open Camo on both devices

### 3. Network Camera App

This allows wireless connection:

- Install a camera streaming app on your iPhone (like IP Camera Lite)
- Connect both your Mac and iPhone to the same Wi-Fi network
- In the app, set up streaming and note the URL
- Run the object detector with the URL parameter

For detailed instructions on connecting your iPhone camera, run:

```bash
python iphone_connection.py
```

## Controls

While the object detector is running:

- **ESC**: Exit the program
- **Space**: Manually trigger detection
- **a**: Toggle automatic detection mode

## Project Structure

```
Object_Detection/
├── object_detector.py     # Main script
├── iphone_connection.py   # iPhone camera connection helper
├── requirements.txt       # Dependencies
├── README.md              # This file
└── src/                   # Source code
    ├── __init__.py        # Package initialization
    ├── main.py            # Main implementation
    ├── detector.py        # Object detector class
    ├── camera_utils.py    # Camera utilities
    ├── api_utils.py       # API key utilities
    └── iphone_connection.py  # iPhone connection details
```

## Customization

You can customize the system by modifying the following parameters in `src/detector.py`:

- `DEFAULT_DETECTION_INTERVAL`: Time between automatic detections (seconds)
- `DEFAULT_CONFIDENCE_THRESHOLD`: Minimum confidence score for displaying detections
- `COLORS`: Color mapping for different object categories

## Acknowledgments

This project was built using:
- OpenAI's GPT-4o for object detection
- OpenCV for camera input and visualization
- Apple's Continuity Camera for iPhone integration

## License

This project is available under the MIT License. See the LICENSE file for details. 