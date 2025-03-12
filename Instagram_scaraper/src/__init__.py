"""
Instagram Scraper package.

This package contains modules for scraping images from Instagram.
"""

from .browser import connect_to_existing_browser, scroll_to_bottom, wait_for_instagram_page
from .image_extractor import extract_image_urls
from .downloader import download_images, save_page_source

__all__ = [
    'connect_to_existing_browser',
    'scroll_to_bottom',
    'wait_for_instagram_page',
    'extract_image_urls',
    'download_images',
    'save_page_source'
] 