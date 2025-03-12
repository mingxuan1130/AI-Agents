"""
Module for extracting abstracts from paper pages.
"""
import requests
from bs4 import BeautifulSoup
import re

def get_paper_abstract(paper_url):
    """
    Fetch the abstract from the paper's page.
    
    Args:
        paper_url (str): URL of the paper page
        
    Returns:
        str: The extracted abstract or "Abstract not available" if not found
    """
    try:
        response = requests.get(paper_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple ways to find the abstract
        # Method 1: Look for dt/dd pair
        abstract_dt = soup.find('dt', string=re.compile('Abstract', re.I))
        if abstract_dt and abstract_dt.find_next_sibling('dd'):
            return abstract_dt.find_next_sibling('dd').text.strip()
        
        # Method 2: Look for div with id abstract
        abstract_div = soup.find('div', {'id': 'abstract'})
        if abstract_div:
            return abstract_div.text.strip()
        
        # Method 3: Look for div with class abstract
        abstract_div = soup.find('div', {'class': 'abstract'})
        if abstract_div:
            return abstract_div.text.strip()
        
        return "Abstract not available"
    except Exception as e:
        print(f"Error fetching abstract: {str(e)}")
        return "Abstract not available" 