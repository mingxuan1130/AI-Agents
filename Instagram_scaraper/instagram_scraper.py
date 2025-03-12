#!/usr/bin/env python3
"""
Instagram Scraper

A tool to scrape images from Instagram accounts using an existing Chrome browser.
"""

import os
import time
import argparse
from datetime import datetime
import subprocess

from src.browser import connect_to_existing_browser, scroll_to_bottom, wait_for_instagram_page
from src.image_extractor import extract_image_urls
from src.downloader import download_images, save_page_source

def main():
    """Main function to run the Instagram scraper."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Scrape images from Instagram accounts using an existing Chrome window'
    )
    parser.add_argument(
        '--account', '-a', 
        type=str, 
        default='uchicago',
        help='Instagram account name to scrape (default: uchicago)'
    )
    parser.add_argument(
        '--output', '-o', 
        type=str, 
        default='instagram_images',
        help='Output directory for downloaded images (default: instagram_images)'
    )
    parser.add_argument(
        '--max-scrolls', 
        type=int, 
        default=20,
        help='Maximum number of scrolls to perform (default: 20)'
    )
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Save page source for debugging'
    )
    args = parser.parse_args()
    
    # Create a more organized folder structure
    # Main downloads folder
    main_folder = args.output
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    
    # Create a subfolder with account name and date
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_directory = os.path.join(main_folder, f'{args.account}_{current_date}')
    
    print(f'Target Instagram account: @{args.account}')
    print(f'Images will be saved to: {output_directory}')
    
    try:
        # Connect to the existing Chrome browser
        driver = connect_to_existing_browser()
        
        # Wait for the user to navigate to the Instagram account page
        wait_for_instagram_page(driver, account_name=args.account)
        
        # Wait for the page to fully load
        time.sleep(5)
        
        # Scroll through the page to load all images
        print('Scrolling through the page to load all images...')
        scroll_to_bottom(driver, max_scrolls=args.max_scrolls)
        
        # Save page source for debugging if requested
        if args.debug:
            page_source_path = save_page_source(driver, output_directory)
        
        # Extract image URLs
        print('Extracting image URLs...')
        image_urls = extract_image_urls(driver)
        
        print(f'Found {len(image_urls)} unique images')
        
        if image_urls:
            # Download images
            print('Downloading images...')
            successful, failed = download_images(
                image_urls, 
                output_directory, 
                prefix=f"{args.account}_image"
            )
            
            # Print summary
            print('\nDownload summary:')
            print(f'- Successfully downloaded: {successful} images')
            print(f'- Failed to download: {failed} images')
            print(f'- Total attempted: {len(image_urls)} images')
            print(f'Images saved to: {os.path.abspath(output_directory)}')
            
            # Open the folder if any images were downloaded
            if successful > 0:
                print('Opening download folder...')
                try:
                    # For macOS
                    if os.name == 'posix':
                        subprocess.run(['open', output_directory], check=False)
                    # For Windows
                    elif os.name == 'nt':
                        os.startfile(output_directory)
                except Exception as e:
                    print(f'Could not open folder: {str(e)}')
        else:
            print('No images found to download.')
            if args.debug:
                print(f'Check the page source at: {os.path.abspath(page_source_path)} for debugging')
        
        print('Process complete!')
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        # Close the driver but don't quit the browser
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    main() 