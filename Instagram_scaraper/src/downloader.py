"""
Downloader module for Instagram scraper.

This module contains functions for downloading images and saving page source.
"""

import os
import time
import random
import requests

def download_images(urls, output_dir, prefix="instagram_image"):
    """
    Download images from the extracted URLs.
    
    Args:
        urls (list): List of image URLs to download.
        output_dir (str): Directory to save the downloaded images.
        prefix (str, optional): Prefix for the image filenames. Defaults to "instagram_image".
        
    Returns:
        tuple: A tuple containing (successful_downloads, failed_downloads).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a log file to keep track of downloaded images
    log_file_path = os.path.join(output_dir, 'download_log.txt')
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Download started at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Total images to download: {len(urls)}\n\n")
    
    successful_downloads = 0
    failed_downloads = 0
    
    for i, url in enumerate(urls, 1):
        try:
            # Add headers to appear more like a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.instagram.com/'
            }
            
            response = requests.get(url, stream=True, headers=headers)
            if response.status_code == 200:
                # Extract file extension from URL or default to .jpg
                file_extension = '.jpg'
                if '.' in url.split('?')[0].split('/')[-1]:
                    possible_ext = '.' + url.split('?')[0].split('/')[-1].split('.')[-1].lower()
                    if possible_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        file_extension = possible_ext
                
                # Create a more descriptive filename
                filename = f'{prefix}_{i:03d}{file_extension}'
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Get file size
                file_size = os.path.getsize(filepath)
                file_size_kb = file_size / 1024
                
                print(f'Downloaded: {filename} ({file_size_kb:.1f} KB)')
                
                # Log the successful download
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"✓ {filename}: {url} ({file_size_kb:.1f} KB)\n")
                
                successful_downloads += 1
                
                # Add a small delay between downloads to avoid rate limiting
                time.sleep(random.uniform(0.5, 1.5))
            else:
                print(f'Failed to download image {i}: Status code {response.status_code}')
                # Log the failed download
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"✗ Image {i}: Failed with status code {response.status_code}\n")
                
                failed_downloads += 1
        except Exception as e:
            print(f'Error downloading image {i}: {str(e)}')
            # Log the error
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"✗ Image {i}: Error - {str(e)}\n")
            
            failed_downloads += 1
    
    # Write summary to log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"\nDownload completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Successful downloads: {successful_downloads}\n")
        log_file.write(f"Failed downloads: {failed_downloads}\n")
    
    return successful_downloads, failed_downloads

def save_page_source(driver, output_dir):
    """
    Save the page source for debugging purposes.
    
    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        output_dir (str): Directory to save the page source.
        
    Returns:
        str: Path to the saved page source file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    page_source_path = os.path.join(output_dir, 'page_source.html')
    with open(page_source_path, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    print(f"Page source saved to: {page_source_path}")
    return page_source_path 