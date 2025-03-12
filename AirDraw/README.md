# AirDraw - Gesture Drawing Application

AirDraw is an interactive application that allows you to draw in the air using just your finger. The application uses your webcam and hand tracking technology to detect finger movements and convert them into digital drawings.

## Project Overview

This project uses computer vision and hand tracking technology to create a virtual drawing canvas. By tracking the movement of your index finger, the application allows you to draw in the air as if you were drawing on a physical canvas. The application features a user-friendly interface with various drawing tools and effects.

## Features

- **Draw with your index finger** in the air
- **Multiple colors** to choose from
- **Drawing modes**: Draw or Erase
- **Line styles**: Continuous lines or Dots
- **Special effects**: None, Rainbow, or Glow
- **Adjustable brush size**
- **Interactive UI** with clickable buttons

## Requirements

- Python 3.6+
- OpenCV
- NumPy
- MediaPipe
- A webcam

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/airdraw.git
   cd airdraw
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python airdraw.py
   ```

## How to Use

### Hand Gestures

- **Draw**: Hold your index finger up and keep it separated from your middle finger
- **Stop Drawing**: Bring your index and middle fingers close together (pinch gesture)

### UI Controls

The application features a user-friendly interface with clickable buttons:

- **Color Palette**: Click on any color box at the top-left to change your drawing color
- **Mode**: Toggle between Draw and Erase modes
- **Style**: Toggle between Line (continuous) and Dots drawing styles
- **Effect**: Cycle through special effects (None, Rainbow, Glow)
- **Size**: Displays the current brush thickness
- **-/+**: Click - to decrease or + to increase brush thickness
- **CLEAR**: Clear the entire canvas
- **EXIT**: Close the application

### iPhone Camera Connection

If you're using a Mac with an iPhone, you can use your iPhone as a webcam for this application:

1. Ensure both your Mac and iPhone are running the latest versions of their respective operating systems
2. Make sure both devices are signed in to the same Apple ID
3. Enable Wi-Fi and Bluetooth on both devices
4. Place your iPhone near your Mac
5. Your Mac should automatically detect your iPhone as a camera option
6. The application will use the iPhone camera if it's selected as the default camera

### Tips for Best Results

1. Use the application in a well-lit environment
2. Position yourself so that your hand is clearly visible to the webcam
3. Keep your hand movements steady for smoother lines
4. Experiment with different effects and brush sizes for creative results
5. If the hand tracking is unstable, try adjusting your distance from the camera

## Troubleshooting

- **Camera not detected**: Ensure your webcam is properly connected and not being used by another application
- **Hand not tracking well**: Improve lighting conditions and make sure your hand is clearly visible
- **Performance issues**: Close other resource-intensive applications running in the background
- **iPhone camera not connecting**: Make sure both devices are on the same Wi-Fi network and Bluetooth is enabled

## Keyboard Shortcuts

- **ESC**: Emergency exit from the application

## Project Structure

- `airdraw.py`: Main application file
- `hand_tracking.py`: Hand tracking functionality using MediaPipe
- `drawing_utils.py`: Drawing canvas and drawing operations
- `ui_manager.py`: User interface management
- `requirements.txt`: Required Python packages

## License

This project is open-source and available for personal and educational use.

## Acknowledgments

This application uses MediaPipe for hand tracking technology. 