# Instagram Scraper

A modular and reliable tool to scrape images from Instagram accounts using an existing Chrome browser with remote debugging enabled.

## Project Overview

This tool allows you to scrape images from any Instagram account by connecting to an already opened Chrome browser. This approach has several advantages:
- It allows you to log in to Instagram manually before scraping
- It bypasses many of Instagram's anti-scraping measures
- It provides a more reliable way to extract images compared to fully automated approaches

The project is organized in a modular way, with separate components for:
- Browser interaction and navigation
- Image URL extraction
- Image downloading and saving

## Features

- Connect to an existing Chrome browser with remote debugging enabled
- Navigate to any Instagram account
- Scroll through the page to load all images
- Extract image URLs using multiple methods for maximum coverage
- Download all images to a folder organized by account name and date
- Create a detailed log file of the download process
- Works on macOS, Windows, and Linux

## Prerequisites

- Python 3.6 or higher
- Google Chrome browser installed
- Required Python packages: `selenium`, `requests`

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Follow these steps to scrape images from an Instagram account:

1. Start Chrome with remote debugging enabled:

```bash
bash start_chrome_for_scraping.sh
```

2. In the opened Chrome window, navigate to the Instagram account you want to scrape (e.g., https://www.instagram.com/uchicago/)
3. Log in to Instagram if prompted
4. Run the scraper:

```bash
python instagram_scraper.py --account uchicago
```

### Command Line Options

You can use these options with the scraper:

- `--account` or `-a`: Instagram account name to scrape (default: "uchicago")
- `--output` or `-o`: Output directory for downloaded images (default: "instagram_images")
- `--max-scrolls`: Maximum number of scrolls to perform (default: 20)
- `--debug`: Save page source for debugging

Example:

```bash
python instagram_scraper.py --account natgeo --output natgeo_images --max-scrolls 30 --debug
```

## Project Structure

```
Instagram_scraper/
├── instagram_scraper.py     # Main script
├── start_chrome_for_scraping.sh  # Script to start Chrome with debugging
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── src/                     # Source code modules
    ├── __init__.py          # Package initialization
    ├── browser.py           # Browser interaction functions
    ├── image_extractor.py   # Image URL extraction functions
    └── downloader.py        # Image downloading functions
```

## How It Works

1. The script connects to an already opened Chrome browser with remote debugging enabled
2. It waits for you to navigate to the specified Instagram account
3. It scrolls through the page to load all images
4. It extracts image URLs using multiple methods
5. It downloads all images to a folder organized by account name and date
6. It creates a log file with details of the download process

## Troubleshooting

If you encounter issues:

1. **No Images Found**: Try increasing the number of scrolls with `--max-scrolls` to load more images.

2. **Connection Issues**: Make sure Chrome is running with remote debugging enabled on port 9222.

3. **Selenium WebDriver Issues**: Make sure you have the latest version of Chrome and the appropriate ChromeDriver installed.

4. **Instagram Changes**: Instagram may change their website structure. If the scraper stops working, check for updates or report the issue.

## Notes

- This scraper is designed for educational purposes only
- Use responsibly and respect Instagram's terms of service 