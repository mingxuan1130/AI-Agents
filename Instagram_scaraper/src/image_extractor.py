"""
Image extractor module for Instagram scraper.

This module contains functions for extracting image URLs from Instagram pages.
"""

from selenium.webdriver.common.by import By

def extract_image_urls(driver):
    """
    Extract image URLs from the Instagram page.
    
    Uses multiple methods to find image URLs to ensure maximum coverage.
    
    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        
    Returns:
        list: A list of unique image URLs.
    """
    print("Extracting image URLs...")
    
    # Try multiple methods to find images
    image_urls = set()
    
    # Method 1: Find all img elements
    images = driver.find_elements(By.TAG_NAME, 'img')
    for img in images:
        try:
            src = img.get_attribute('src')
            if src and ('scontent' in src or 'cdninstagram' in src):
                image_urls.add(src)
        except Exception as e:
            print(f"Error extracting URL from an image: {e}")
    
    # Method 2: Find images in article elements (Instagram posts)
    try:
        articles = driver.find_elements(By.TAG_NAME, 'article')
        for article in articles:
            try:
                imgs = article.find_elements(By.TAG_NAME, 'img')
                for img in imgs:
                    src = img.get_attribute('src')
                    if src and ('scontent' in src or 'cdninstagram' in src):
                        image_urls.add(src)
            except:
                continue
    except:
        pass
    
    # Method 3: Find images in div elements with specific classes
    try:
        # Common Instagram image container classes
        for class_name in ['_aagv', '_aagu', '_aag_']:
            try:
                divs = driver.find_elements(By.CLASS_NAME, class_name)
                for div in divs:
                    try:
                        imgs = div.find_elements(By.TAG_NAME, 'img')
                        for img in imgs:
                            src = img.get_attribute('src')
                            if src and ('scontent' in src or 'cdninstagram' in src):
                                image_urls.add(src)
                    except:
                        continue
            except:
                continue
    except:
        pass
    
    # Method 4: Use JavaScript to find all images
    try:
        js_images = driver.execute_script("""
            var images = [];
            var imgElements = document.getElementsByTagName('img');
            for (var i = 0; i < imgElements.length; i++) {
                var src = imgElements[i].src;
                if (src && (src.includes('scontent') || src.includes('cdninstagram'))) {
                    images.push(src);
                }
            }
            return images;
        """)
        for src in js_images:
            image_urls.add(src)
    except Exception as e:
        print(f"Error executing JavaScript to find images: {e}")
    
    return list(image_urls) 